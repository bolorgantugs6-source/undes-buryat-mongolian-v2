#!/usr/bin/env python3
"""Only publish records with reviewer, reviewed date, attributed license and Mongolian text."""
import argparse,csv,json,pathlib,datetime
P=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--output',default='data/reviewed_dictionary.json');a=p.parse_args()
with open(a.csv,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
valid=[];rejected=[];seen=set()
for idx,r in enumerate(rows,2):
 if r.get('translation_status') not in ('reviewed','approved') or not all(r.get(k,'').strip() for k in ['buryat','mongolian','reviewer','reviewed_at','source','license']):rejected.append(idx);continue
 try:datetime.date.fromisoformat(r['reviewed_at'])
 except ValueError:rejected.append(idx);continue
 k=(r['buryat'].casefold().strip(),r['mongolian'].casefold().strip())
 if k in seen:continue
 seen.add(k)
 valid.append({**r,'status':'reviewed','part_of_speech':r.get('part_of_speech','')})
out=P/a.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(valid,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'approved_exported':len(valid),'rejected_rows':len(rejected),'file':str(out)},indent=2))
