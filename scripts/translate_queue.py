#!/usr/bin/env python3
"""Optional paid translation of candidate Buryat word forms into Mongolian drafts.
Requires GOOGLE_TRANSLATE_KEY environment secret and user acknowledgement of paid usage.
"""
import argparse,csv,json,os,time,urllib.parse,urllib.request,pathlib
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--output',default='data/lexicon_machine_drafts.csv');p.add_argument('--limit',type=int,default=100);p.add_argument('--execute',action='store_true');a=p.parse_args()
if not a.execute:raise SystemExit('Dry run only. To make billable calls, explicitly pass --execute and GOOGLE_TRANSLATE_KEY.')
key=os.getenv('GOOGLE_TRANSLATE_KEY');
if not key:raise SystemExit('GOOGLE_TRANSLATE_KEY is required; never commit it.')
with open(a.source,encoding='utf-8-sig',newline='') as fp:rows=list(csv.DictReader(fp))
out=[]
for r in rows:
 if len(out)>=a.limit:break
 if r.get('mongolian','').strip():continue
 data=urllib.parse.urlencode({'q':r['buryat'],'source':'bua','target':'mn','format':'text'}).encode()
 req=urllib.request.Request('https://translation.googleapis.com/language/translate/v2?key='+urllib.parse.quote(key),data=data,headers={'Content-Type':'application/x-www-form-urlencoded'})
 try:
  with urllib.request.urlopen(req,timeout=30) as response: payload=json.load(response)
  translation=payload['data']['translations'][0]['translatedText']
 except Exception as exc:print('API failed, stopping:',type(exc).__name__,str(exc)[:100]);break
 r.update(mongolian=translation,translation_status='machine_draft',reviewer='',reviewed_at='');out.append(r)
output=pathlib.Path(a.output);output.parent.mkdir(parents=True,exist_ok=True)
with output.open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(out)
print('Machine drafts generated:',len(out),'Unreviewed. Review before publication.')
