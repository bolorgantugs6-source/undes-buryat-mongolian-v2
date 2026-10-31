#!/usr/bin/env python3
"""Import licensed Buryat–Russian parallel corpus to Vercel static shards.
Usage: pip install pyarrow; python scripts/import_parallel.py DATA.parquet
Does NOT assert the sentences have Mongolian translations or human verification.
"""
import argparse,csv,json,pathlib,re,hashlib,collections
root=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--license',default='cc-by-4.0');p.add_argument('--attribution',default='Sarana Abidueva et al., Buryat–Russian parallel corpus, Hugging Face');p.add_argument('--max-rows',type=int,default=120000);a=p.parse_args()
path=pathlib.Path(a.source);out=root/'public'/'parallel';out.mkdir(parents=True,exist_ok=True)
if path.suffix=='.parquet':
 try:import pyarrow.parquet as pq
 except ImportError:raise SystemExit('Install pyarrow: pip install pyarrow')
 rows=pq.read_table(path).to_pylist()
elif path.suffix=='.csv':
 with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
else:
 rows=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
seen=set();records=[]
for r in rows:
 buriat=str(r.get('bxr') or r.get('bua') or r.get('buryat') or '').strip();russian=str(r.get('ru') or r.get('russian') or '').strip()
 if not buriat or not russian:continue
 key=(buriat,russian)
 if key in seen:continue
 seen.add(key)
 records.append({'id':len(records)+1,'buryat':buriat,'russian':russian,'source':a.attribution,'license':a.license,'translation_status':'source_parallel_russian','mongolian':None,'mongolian_reviewed':False})
 if len(records)>=a.max_rows:break
for old in out.glob('part-*.json'):old.unlink()
chunk=500
for i in range(0,len(records),chunk):
 (out/f'part-{i//chunk+1:04d}.json').write_text(json.dumps(records[i:i+chunk],ensure_ascii=False,separators=(',',':')),encoding='utf-8')
manifest={'count':len(records),'chunks':(len(records)+chunk-1)//chunk,'chunkSize':chunk,'source':a.attribution,'license':a.license,'language_pair':'Buryat-Russian','verified_mongolian_pairs':0,'sha256_source':hashlib.sha256(path.read_bytes()).hexdigest()}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
