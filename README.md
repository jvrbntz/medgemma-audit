# MedGemma-Audit

MedGemma-Audit is an evaluation harness that stress-tests MedGemma 1.5 4B (Google's medical specialized model built on Gemma 3, see [Model Selection](#model-section) below) on clinical text tasks. MedGemma is not clinically validated as of August 2026; this project measures where it fails, how often, and why, so a developer can decide whether it's safe to deploy in a clinical support tool.

**Status:** pre-build

**Intended use:** This is a learning prototype for practicing LLM evaluation methodology, not a clinical tool. It must not be used to inform patient care, diagnosis, or treatment decisions.

## Data

**Status Update (2026-08-20):** dataset exploration found diagnosis leakage in `transcription` field that can't be reliably prevented by header-based stripping (see `notebooks/mtsamples_exploration.ipynb`). MTSamples is being reconsidered for this task; a replacement dataset is under evaluation, not yet finalized.  
**Source:** Data is from [MTSamples](https://www.mtsamples.com/index.asp), a collection of medical note transcriptions from various medical specialties.  
**Acquisition:** The dataset will be acquired via `kagglehub` from [Tara Boyle](https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions), which was put together 8 years ago.  
**Data Size:** 1 file, 6 columns, 17.01 MB.  
**Columns:** 6 (1 index plus 5 fields):

- `description`: short description of transcription
- `medical_specialty`: medical specialty classification of transcription
- `sample_name`: transcription title
- `transcription`: sample medical transcriptions
- `keywords`: relevant keywords from transcription

**License:** Kaggle dataset license - CC0: Public Domain.
**Privacy:** MTSamples states names, locations, and dates were changed in the sample reports.

## Model Selection

MedGemmaAudit uses MedGemma 1.5 4B (`medgemma1.5:4b` via Ollama) rather than the original MedGemma 4B. Version 1.5 leads on medical reasoning (see table below) and on real-world discharge-summary QA (EHRNoteQA: 79.4 → 80.4) — both closer to this project's diagnosis-from-notes task than its one regression, PubMedQA. The original 4B is more established and still ahead on PubMedQA; that comparison is deferred to a v2 head-to-head against this project's own eval.

| Dataset                | MedGemma 1 4B | MedGemma 1.5 4B |
| ---------------------- | ------------- | --------------- |
| MedQA (4-op)           | 64.4          | 69.1            |
| MedMCQA                | 55.7          | 59.8            |
| PubMedQA               | 73.4          | 68.2            |
| MMLU Med               | 70.0          | 69.6            |
| MedXpertQA (text only) | 14.2          | 16.4            |
| AfriMed-QA             | 52.0          | 56.0            |

_source:_ [MedGemma 1.5 model card](https://developers.google.com/health-ai-developer-foundations/medgemma/model-card)

Per Google's model card, outputs "are not intended to directly inform clinical diagnosis, patient management decisions, treatment recommendations, or any other direct clinical practice applications," and should be "considered preliminary and require independent verification, clinical correlation, and further investigation."

## Known Limitations

- **Training-time contamination.** MTSamples has been public for years. MedGemma may have already seen these exact records during training, so a "correct" diagnosis could just be memorization, not real reasoning. This fails silently: nothing in the output tells you which one happened. Fixing it means paraphrasing the input notes, which is its own project and not worth doing before the core pipeline works, so it's a task for a later version.
- **Judge bias and reliability.** v1 uses a local, weaker model as judge instead of a paid external one, to skip the extra cost and credential. That means scores could be biased toward outputs that sound like the judge, or miss reasoning errors the judge isn't strong enough to catch itself. A stronger external judge (Claude or GPT via API) is planned for a later version.
- **Diagnosis leakage led to reconsidering the dataset.** Header coverage for DIAGNOSIS/IMPRESSION/PLAN/ASSESSMENT sections varies from 33% (Office Notes) to 100% (Allergy/Immunology), ~73% for General Medicine, and even where the header matches, some notes still weave the diagnosis through the text with no removable section at all. Expanding the header list further won't fix this, so MTSamples is being reconsidered for this task rather than patched around (see `notebooks/mtsamples_exploration.ipynb`).  

## Key Design Decisions

- **Note:** the dataset and task below reflect the original design. Both are under reconsideration; see Known Limitations above.  
- **Differential diagnosis scored by LLM-as-judge.** MedGemma produces a differential diagnosis with reasoning for each note. A second model judges whether the correct diagnosis and other plausible ones show up, and critiques the reasoning. Chose this over simpler options like exact-match scoring against `medical_specialty`, because it captures ranked clinical reasoning instead of reducing it to one label.
- **Local judge model for v1.** Chose a local Ollama model as judge instead of an external API, to keep v1 free of a paid dependency and a second credential to manage. That means accepting the bias and reliability risk above for now instead of solving it. A stronger external judge is planned for a later version, not ruled out.
