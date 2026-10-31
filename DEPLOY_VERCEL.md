# Deploy ҮНДЭС on Vercel

1. Extract this ZIP. Upload the contents to a GitHub repository.
2. Vercel → Add New Project → Import Git Repository → Deploy (framework: Other; project root).
3. Test Home, About founder, Stories, Dictionary, and Learning pages.
4. The translator backend requires `GOOGLE_TRANSLATE_KEY` in Vercel environment variables; without it, paid live API translation does not work. The current free Colab NLLB model is not included as a Vercel serverless translation service.
5. The reviewed word dataset from Colab is **not included** here because no exported CSV was supplied. Do not advertise 18,400 verified translations yet. `data/reviewed_dictionary.json` contains zero approved pairs.
6. The story section contains 63 bilingual community-feedback records. The project owner reports reviewing the Mongolian texts and receiving positive feedback from a Buryat-speaking friend. This is not independently authenticated editorial verification.
7. To release approved dictionary records, populate `data/reviewed_dictionary.json` using the provided scripts. The API intentionally only publishes records with source, license, reviewer and status=reviewed.

Founder photo: `public/bolor-gantugs-founder.webp`.
