"""Rebuild customer intelligence from the complete UCI Online Retail II workbook."""
import argparse, hashlib, json, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

def score(s, reverse=False):
    # Equal observed values always receive equal scores; bins need not be equal size.
    cuts=s.quantile([.2,.4,.6,.8]).values
    v=pd.Series(np.searchsorted(cuts,s,side='left')+1,index=s.index)
    return 6-v if reverse else v

def build(source, root):
    out=Path(root);private=out/'data/private';public=out/'tableau'
    private.mkdir(parents=True,exist_ok=True);public.mkdir(parents=True,exist_ok=True)
    frames=pd.read_excel(source,sheet_name=None)
    raw=pd.concat(frames.values(),ignore_index=True)
    raw.columns=raw.columns.str.replace(' ','',regex=False)
    raw=raw.rename(columns={'CustomerID':'customer_id','Invoice':'invoice','StockCode':'stock','InvoiceDate':'date','Quantity':'quantity','Price':'price','Country':'country'})
    raw['date']=pd.to_datetime(raw.date,errors='coerce')
    raw['invoice']=raw.invoice.astype('string').str.strip().str.upper()
    for c in ['price','quantity']:raw[c]=pd.to_numeric(raw[c],errors='coerce')
    audit={'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),'raw_rows':len(raw),'sheets':{k:len(v) for k,v in frames.items()},'missing_by_column':raw.isna().sum().to_dict(),'exact_duplicate_rows':int(raw.duplicated().sum()),'cancellation_rows':int(raw.invoice.str.startswith('C',na=False).sum()),'negative_quantity_rows':int(raw.quantity.lt(0).sum()),'nonpositive_price_rows':int(raw.price.le(0).sum()),'date_min':str(raw.date.min()),'date_max':str(raw.date.max())}
    d=raw.drop_duplicates().copy()
    valid=d.customer_id.notna() & d.invoice.notna() & d.date.notna() & d.quantity.gt(0) & d.price.gt(0) & ~d.invoice.str.startswith('C',na=False)
    d=d[valid].copy();d['revenue_pence']=(d.quantity*d.price*100).round().astype('int64')
    # De-identify exports; mapping and source stay private. Not a formal anonymization claim.
    d['customer_key']=d.customer_id.astype('int64').astype(str).map(lambda x:hashlib.sha256(('uci502-portfolio:'+x).encode()).hexdigest()[:16])
    observation=d.date.max().normalize()+pd.Timedelta(days=1)
    cust=d.groupby('customer_key').agg(last_purchase=('date','max'),first_purchase=('date','min'),frequency=('invoice','nunique'),monetary_pence=('revenue_pence','sum'),product_count=('stock','nunique'))
    cust['recency_days']=(observation-cust.last_purchase.dt.normalize()).dt.days
    # Most recent observed country; ties sorted lexically for deterministic assignment.
    countries=d.sort_values(['date','invoice','country']).drop_duplicates('customer_key',keep='last').set_index('customer_key').country
    cust['country']=countries;cust['country_count']=d.groupby('customer_key').country.nunique()
    for letter,col,rev in [('R','recency_days',True),('F','frequency',False),('M','monetary_pence',False)]:cust[letter]=score(cust[col],rev)
    cust['rfm_score']=cust[['R','F','M']].astype(str).agg(''.join,axis=1)
    r,f,m=cust.R,cust.F,cust.M
    cust['segment']=np.select([(r>=4)&(f>=4)&(m>=4),(r<=2)&((f>=4)|(m>=4)),(r>=3)&(f>=4),(r>=4)&(f>=2),(r>=4)&(f==1),(r<=2)&(f<=2)],['Champions','At Risk','Loyal Customers','Potential Loyalists','New / Recent','Hibernating'],default='Needs Attention')
    cust['action']=cust.segment.map({'Champions':'Reward and retain','At Risk':'Investigate and reactivate','Loyal Customers':'Develop account depth','Potential Loyalists':'Encourage next purchase','New / Recent':'Onboard','Hibernating':'Test low-cost reactivation','Needs Attention':'Test engagement'})
    cust['monetary_gbp']=cust.monetary_pence/100;cust['repeat_customer']=(cust.frequency>=2).astype(int)
    cust['value_band']=pd.cut(cust.monetary_gbp,[-np.inf,100,500,1000,5000,np.inf],labels=['Up to £100','£100–500','£500–1,000','£1,000–5,000','Over £5,000']).astype(str)
    tx=d[['customer_key','invoice','date','stock','country','quantity','price','revenue_pence']].copy()
    tx.to_csv(private/'cleaned_transactions.csv',index=False)
    cust.reset_index().to_csv(private/'customers.csv',index=False)
    cust.reset_index()[['customer_key','recency_days','frequency','monetary_gbp','R','F','M','rfm_score','segment']].to_csv(private/'rfm_scoring.csv',index=False)
    # Single shared customer source; customers counted once under their latest country.
    cust.reset_index().to_csv(public/'customers.csv',index=False)
    monthly=d.assign(month=d.date.dt.strftime('%Y-%m')).groupby('month').agg(revenue_pence=('revenue_pence','sum'),orders=('invoice','nunique'),active_customers=('customer_key','nunique')).reset_index()
    monthly.to_csv(public/'monthly.csv',index=False)
    seg=cust.groupby(['country','segment','action'],dropna=False).agg(customers=('frequency','size'),orders=('frequency','sum'),revenue_gbp=('monetary_gbp','sum'),recency_total=('recency_days','sum'),repeat_customers=('repeat_customer','sum')).reset_index()
    seg.to_csv(public/'country_segments.csv',index=False)
    # Co-purchase product pair support, not inferred product categories or conversion rates.
    top=d.groupby('stock').invoice.nunique().nlargest(30).index
    baskets=d[d.stock.isin(top)][['invoice','stock']].drop_duplicates()
    pairs=baskets.merge(baskets,on='invoice',suffixes=('_a','_b'))
    pairs=pairs[pairs.stock_a.astype(str)<pairs.stock_b.astype(str)]
    pairs=pairs.groupby(['stock_a','stock_b']).invoice.nunique().rename('co_purchase_orders').nlargest(20).reset_index()
    pairs['eligible_orders']=d.invoice.nunique();pairs['support']=pairs.co_purchase_orders/pairs.eligible_orders
    pairs.to_csv(public/'cross_sell_pairs.csv',index=False)
    with sqlite3.connect(private/'analytics.sqlite') as con:
        tx.to_sql('transactions',con,index=False,if_exists='replace');cust.reset_index().to_sql('customers',con,index=False,if_exists='replace')
        sql=(Path(__file__).resolve().parents[1]/'sql/analysis.sql').read_text()
        results={}
        for i,q in enumerate(sql.split(';')):
            if q.strip():results[f'query_{i+1}']=pd.read_sql_query(q,con).to_dict(orient='records')
    # Independent SQL customer aggregation and integer currency reconciliation.
        independently=pd.read_sql_query('SELECT customer_key, COUNT(DISTINCT invoice) frequency, SUM(revenue_pence) monetary_pence FROM transactions GROUP BY customer_key',con).set_index('customer_key')
    assert independently.sort_index()[['frequency','monetary_pence']].equals(cust.sort_index()[['frequency','monetary_pence']])
    assert int(cust.monetary_pence.sum())==int(tx.revenue_pence.sum())
    assert cust.frequency.sum()==tx.invoice.nunique(), 'Invoice assigned to multiple customers'
    assert seg.customers.sum()==len(cust) and abs(seg.revenue_gbp.sum()-cust.monetary_gbp.sum())<.001
    assert cust[['R','F','M']].ge(1).all().all() and cust[['R','F','M']].le(5).all().all()
    audit.update(eligible_rows=len(d),customers=len(cust),orders=int(tx.invoice.nunique()),revenue_gbp=float(cust.monetary_gbp.sum()),observation_date=str(observation.date()),repeat_customer_share=float(cust.repeat_customer.mean()),customers_multiple_countries=int(cust.country_count.gt(1).sum()),score_cutpoints={c:cust[c].quantile([.2,.4,.6,.8]).to_dict() for c in ['recency_days','frequency','monetary_pence']},checks={'sql_customer_reconciliation':True,'integer_revenue_reconciliation':True,'invoice_customer_uniqueness':True,'segment_reconciliation':True})
    (out/'docs/audit.json').write_text(json.dumps(audit,indent=2,default=str));(out/'docs/sql_results.json').write_text(json.dumps(results,indent=2,default=str))
    print(json.dumps(audit,indent=2,default=str))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',default='.');a=p.parse_args();build(a.input,a.output)
