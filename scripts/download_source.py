#!/usr/bin/env python3
from urllib.request import urlretrieve
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
url='https://huggingface.co/datasets/SaranaAbidueva/buryat-russian_parallel_corpus/resolve/main/data/train-00000-of-00001-9cc025291cfbcfe4.parquet'
target=root/'data'/'source_buryat_russian.parquet'
urlretrieve(url,target)
subprocess.check_call([sys.executable,str(root/'scripts'/'import_parallel.py'),str(target)])
subprocess.check_call([sys.executable,str(root/'scripts'/'build_lexicon.py'),str(target)])
