# ҮНДЭС — lexical extraction and review pipeline

This release adds a **working** corpus-to-dictionary processing path to the existing Vercel site. It does **not** include 18,400 verified pairs. To populate it, download the upstream licensed corpus and run:

```bash
pip install pyarrow
python scripts/download_source.py
# outputs public/parallel/part-*.json + data/lexicon_review_queue.csv
```

You can also run `python scripts/build_lexicon.py data/your_corpus.csv --limit 18400`. It reads Buryat–Russian sentences, counts real Buryat word forms, deduplicates, and includes the original sentence plus Russian aligned context. **Surface forms are not automatically lemmas**; grammatical tagging is left empty when unsupported. The review queue is not a reviewed dictionary.

Optionally run `python scripts/translate_queue.py data/lexicon_review_queue.csv --limit 100 --execute` after supplying the private `GOOGLE_TRANSLATE_KEY` secret and accepting Google Cloud Translation billing. These become **machine drafts**, not reviewed translations. Alternatively, add Mongolian translations in a spreadsheet.

A human reviewer may set `translation_status=reviewed` with real `reviewer` and ISO `reviewed_at` fields after checking each Buryat/Mongolian pair. Then:

```bash
python scripts/publish_approved.py data/lexicon_review_queue.csv
```

Only rows with Mongolian translation, attribution, license, and review metadata are published in `data/reviewed_dictionary.json` and exposed via `/api/dictionary` on Vercel. Sources require license compatibility and attribution. **Do not add invented reviewer names.** The 63 story versions remain in the project; retain review attribution separately.

A 120,000-pair corpus is listed in public catalogs, but this preset reproducibly targets the *SaranaAbidueva* CC BY 4.0 dataset. If your source file has different field names, normalize to `buryat,russian` first.
