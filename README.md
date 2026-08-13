# MedGemma-Audit

MedGemma-Audit is an evaluation harness that stress-tests MedGemma 4B (Google's medical specialized model built on Gemma 3, see [Model Selection](#model-section) below) on clinical text tasks. MedGemma is not clinically validated as of August 2026; this project measures where it fails, how often, and why, so a developer can decide whether it's safe to deploy in a clinical support tool.

**Status:** pre-build

## Data

**Source:** Data is from [MTSamples](https://www.mtsamples.com/index.asp), a collection of medical note transcriptions from various medical specialties.  
**Acquisition:** The dataset will be acquired via `kagglehub` from [Tara Boyle](https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions), which was put together 8 years ago.  
**Data Size:** 1 file, 6 columns, 17.01 MB.  
**Columns:** 6 (1 index plus 5 fields):

- `description`: short description of transcription
- `medical_specialty`: medical specialty classification of transcription
- `sample_name`: transcription title
- `transcription`: sample medical transcriptions
- `keywords`: relevant keywords from transcription

**License:** Kaggle license is CC0: Public Domain.  
**Privacy:** The MTSamples transcriptions have been de-identified of Private Healthcare Information (PHI).

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
