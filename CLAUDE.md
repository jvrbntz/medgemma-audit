# MedGemma-Audit

**Status note (2026-08-20):** the dataset and task below are under reconsideration. See README's Data section and `notebooks/mtsamples_exploration.ipynb`.

## Problem

MedGemma 1.5 4B is not clinically validated. This project measures where its differential-diagnosis output fails, how often, and why, on MTSamples clinical notes — so a developer building on MedGemma can decide whether it's safe to deploy in a clinical support tool. Full pitch: `README.md`.

## MVP

Run a handful of MTSamples records through preprocessing (strip the section where the diagnosis is present) → MedGemma via Ollama (differential diagnosis + reasoning) → a local LLM judge (scores correct-diagnosis presence, differential breadth, reasoning quality). No dashboard, no batch scaling, no contamination mitigation in v1 — see README's Known Limitations.

## Stack

- Python 3.13, managed with `uv`
- `kagglehub` for dataset acquisition
- MedGemma 1.5 4B served locally via Ollama (`medgemma1.5:4b`)
- Judge model: local via Ollama for v1 (specific model TBD); external API (Claude/GPT) planned for v2

## Repo structure

- `src/medgemma_audit/` — package code
- `data/` — gitignored, holds the acquired MTSamples CSV (populated by `acquire_data.py`)
- `evaluations/`, `notebooks/`, `tests/` — currently empty, reserved for eval outputs, exploration, and the test suite

## Component pipeline (build order)

1. **Data acquisition** — done (`src/medgemma_audit/acquire_data.py`)
2. **Preprocessing** — not started. Cleans the raw CSV, strips the diagnosis/assessment section per record (leakage prevention), structures records with non-PHI-shaped field names.
3. **Ollama/LLM connection** — not started. Sends a record's cleaned text to MedGemma, gets differential diagnosis + reasoning back.
4. **Output recording** — not started. Persists MedGemma's output per record.
5. **LLM-as-judge evaluation** — not started. Scores recorded output; needs its own model connection (local for v1).

## Known failure modes

Documented in full, with clinical-cost framing, in README's Known Limitations section:

1. Training-time contamination — MedGemma may have memorized MTSamples during pretraining (it's long-public).
2. Judge self-preference / reliability risk — v1 judge is local and non-frontier.
3. Incomplete diagnosis-stripping — a single heuristic may not cover all ~40 specialty note formats in MTSamples.