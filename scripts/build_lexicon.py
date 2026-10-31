#!/usr/bin/env python3
"""Extract *candidate* Buryat lexical forms from licensed Buryat–Russian aligned text.
Never equates inflected surface forms with verified lemmas; never invents Mongolian translations.
Input CSV / JSONL / Parquet rows with columns bxr/bua/buryat and ru/russian.
"""
import argparse, csv, json, re, pathlib, collections, hashlib
P=pathlib.Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('source');a.add_argument('--min-frequency',type=int,default=1);a.add_argument('--limit',type=int,default=18400);a.add_argument('--source-name',default='Buryat–Russian aligned corpus');a.add_argument('--license',default='cc-by-4.0');a.add_argument('--out',default='data/lexicon_review_queue.csv');args=a.parse_args()
f=pathlib.Path(args.source)
if f.suffix=='.parquet':
 try: import pyarrow.parquet as pq
 except ImportError:raise SystemExit('Install pyarrow: pip install pyarrow')
 rows=pq.read_table(f).to_pylist()
elif f.suffix=='.csv':
 with f.open(encoding='utf-8-sig',newline='') as stream:rows=list(csv.DictReader(stream))
else:
 rows=[json.loads(x) for x in f.read_text(encoding='utf-8').splitlines() if x.strip()]
counts=collections.Counter();examples={};seen_pairs=set(); valid_pairs=0
for row in rows:
 b=str(row.get('buryat') or row.get('bua') or row.get('bxr') or row.get('bur') or '').strip()
 ru=str(row.get('russian') or row.get('ru') or '').strip()
 if not b or not ru or (b,ru) in seen_pairs:continue
 seen_pairs.add((b,ru));valid_pairs+=1
 for token in re.findall(r'[А-Яа-яЁёӨөҮүҺһ]+(?:[\-’\'][А-Яа-яЁёӨөҮүҺһ]+)*',b):
  word=token.casefold();counts[word]+=1
  if word not in examples:examples[word]=(b[:350],ru[:350])
output=P/args.out;output.parent.mkdir(exist_ok=True,parents=True)
with output.open('w',encoding='utf-8-sig',newline='') as stream:
 fields=['id','buryat','mongolian','part_of_speech','lemma','frequency','buryat_example','russian_context','source','license','translation_status','reviewer','reviewed_at','review_notes'];writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
 for idx,(word,n) in enumerate(counts.most_common(),1):
  if n<args.min_frequency or idx>args.limit:break
  ex,ru=examples[word];writer.writerow(dict(id=idx,buryat=word,mongolian='',part_of_speech='',lemma='',frequency=n,buryat_example=ex,russian_context=ru,source=args.source_name,license=args.license,translation_status='needs_translation',reviewer='',reviewed_at='',review_notes=''))
report={'input_pairs':len(rows),'unique_parallel_pairs':valid_pairs,'unique_buryat_surface_forms':len(counts),'review_queue_count':min(args.limit,sum(v>=args.min_frequency for v in counts.values())),'human_verified':0,'note':'Surface words are not morphological lemmas. POS/lemma and Mongolian translations require separate annotation.'}
(P/'data'/'lexicon_extraction_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
