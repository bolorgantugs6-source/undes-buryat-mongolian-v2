#!/usr/bin/env python3
"""Audit batches and build a transparent progress report (not a quality guarantee)."""
import argparse,csv,json,collections
p=argparse.ArgumentParser();p.add_argument('--vocabulary');p.add_argument('--stories');p.add_argument('--out',default='review_report.json');a=p.parse_args()
report={}
if a.vocabulary:
 with open(a.vocabulary,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 dup=len(rows)-len({(r.get('buryat','').strip(),r.get('mongolian','').strip()) for r in rows})
 approved=[r for r in rows if r.get('status')=='reviewed' and r.get('reviewer','').strip() and r.get('mongolian','').strip()]
 flags=[i for i,r in enumerate(rows,2) if r.get('status')=='reviewed' and (not r.get('reviewer','').strip() or not r.get('mongolian','').strip())]
 report['vocabulary']={'total':len(rows),'reviewed_with_attribution':len(approved),'draft_or_incomplete':len(rows)-len(approved),'duplicate_pairs':dup,'invalid_review_rows':flags[:30],'target':18400}
if a.stories:
 with open(a.stories,encoding='utf-8') as f:rows=json.load(f)
 approved=[s for s in rows if s.get('status')=='reviewed' and s.get('rights_verified') and all(str(s.get(k,'')).strip() for k in ['body_buryat','body_mongolian','author','translator','reviewer','license'])]
 report['stories']={'total':len(rows),'reviewed_rights_cleared_bilingual':len(approved),'unfinished':len(rows)-len(approved),'target':63}
with open(a.out,'w',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps(report,ensure_ascii=False,indent=2))
