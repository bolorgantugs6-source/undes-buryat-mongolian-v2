# ҮНДЭС — Vercel edition

This project adapts the existing Buryat ↔ Mongolian website from Cloudflare Workers to Vercel Serverless Functions.

## Contents
- `/public/index.html`: original responsive website with study tools.
- `/public/story_drafts.json`: 63 original Mongolian-only drafts, not 63 bilingual stories.
- `/api/translate.js`: API-key-protected Google Cloud Translation request, Buryat `bua` ↔ Mongolian `mn`.
- `/api/dictionary.js`, `/api/stories.js`, `/api/stats.js`: read-only endpoints publishing only attributed reviewer-approved content.
- `/data/reviewed_dictionary.json`, `/data/reviewed_stories.json`: EMPTY until real reviewed material is available. Do not bulk-insert invented translations.

## Deploy on Vercel
1. Unzip and push the whole project folder to a GitHub repo, or import the project with Vercel CLI.
2. In Vercel → Add New → Project, select the repo. Framework preset: Other. Root directory: repository root. Output directory: `public` (if asked; otherwise leave default for static public assets).
3. Add `GOOGLE_TRANSLATE_KEY` as an environment variable under Project → Settings → Environment Variables, never in public files. Enable Cloud Translation API and billing for that key in Google Cloud.
4. Deploy. Test `/api/stats`, `/api/stories`, `/api/dictionary?q=...`, then a real translation with a short sentence.
5. Configure strict API key restrictions and Google Cloud per-day quotas/budget alerts. **This starter has no persistent per-user rate limiter or bot protection**, so public translation must not be promoted widely until abuse controls are installed.

## Completing the content
- The 18,400 VALIDATED dictionary entries are not present. Obtain appropriately licensed Buryat source entries, draft accurate Mongolian translations, commission competent bilingual review, and record source/license/reviewer before adding reviewed entries to `data/reviewed_dictionary.json`.
- The 63 original Mongolian stories are included as drafts. Translate each into Buryat, review with speakers, ensure publication rights, and then place completed stories in `data/reviewed_stories.json`.
- A functional translation SERVICE is distinct from a validated bilingual dictionary. Machine translations must display as unreviewed.
- Vercel serverless file system is read-only; updates require commit/redeploy. To enable community editing use a persistent database with authentication and moderation.

## Current real metrics
- 63 Mongolian-only drafts.
- 0 native-reviewed bilingual dictionary entries included in this release.
- 0 reviewed Buryat–Mongolian story pairs included.
- Translation backend implemented, not enabled without your private Google Cloud credentials and live deployment.

## Buryat–Russian parallel corpus import (new)

The **Buryat–Russian** source is distinct from the intended **Buryat–Mongolian** dictionary. The `SaranaAbidueva/buryat-russian_parallel_corpus` Hugging Face dataset has 40,979 aligned sentences (CC BY 4.0). It cannot be labeled 18,400 validated Buryat–Mongolian word pairs. The 120,000-pair dataset from another repository is a different collection; check its distribution license independently before importing.

With Python 3 and internet access:

```bash
pip install pyarrow
python scripts/download_source.py
```

Or supply your own rights-cleared `.parquet`, `.csv`, or JSON Lines dataset:

```bash
python scripts/import_parallel.py path/to/data.parquet --attribution 'Source / author' --license 'License'
```

The importer writes paginated static data to `public/parallel/` with source and license attribution and a manifest of actual imported rows. `/api/parallel?page=1` serves the imported Buryat–Russian sentence pairs. It will report zero Mongolian-verified pairs until a real reviewed Buryat–Mongolian file is provided. Do not mark auto-generated pairs reviewed without matching them to your professor's actual records.

For the reviewed 63 *Mongolian* stories, your editorial approval can be recorded, but bilingual publication requires Buryat translations and their corresponding review records.
