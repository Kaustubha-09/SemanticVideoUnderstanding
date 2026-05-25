# Roadmap

Phased plan for turning this from a course-project study into something with broader research utility.

## Phase 1 — Rigor (1–2 weeks)

- Run on the full 141-video, 8-category dataset.
- Bootstrap-resampled confidence intervals on the token-reduction percentage.
- Fix `temperature = 0` for reproducibility.
- Add prompt-sensitivity sweep — 5 prompt variants × the same sample, report which phrasings move the needle.

## Phase 2 — Downstream-task evaluation (2–3 weeks)

- Pair the baseline and diff streams with three downstream tasks:
  1. Single-paragraph video summary (LLM consumes the stream, produces a summary).
  2. Video QA (questions about the events, scored against a reference).
  3. Action classification (predict the activity label from the stream).
- Score downstream-task quality alongside token cost.
- Report Pareto frontier: token cost vs. task accuracy.

## Phase 3 — Multi-model comparison (1 week)

- Replicate the experiment on Claude 3.5 Sonnet (with native vision) and Gemini 1.5 Flash.
- Same prompts, same frames, different models.
- Compare token-reduction generality across providers.

## Phase 4 — Sliding-window context (1 week)

- Replace pairwise diff with a windowed diff: describe the current frame relative to a rolling window of the previous K frames.
- Compare token cost + summary fidelity at K = 1, 3, 5, 10.

## Phase 5 — Adaptive frame sampling (1 week)

- Replace `--frame-interval N` with a perceptual-hash gate: only call the API on frames that differ visually from the last sampled frame by more than a threshold.
- Should reduce token cost further on near-static clips without losing event boundaries.

## Phase 6 — Open data release

- Curate a 50-video micro-benchmark (mixed action types, mixed durations, public-domain or CC licensed).
- Release the dataset + prompts + scoring code as a reproducibility kit.

## Phase 7 — Production-grade client

- Replace `time.sleep(3)` with proper rate-limit-aware async dispatch (`asyncio.Semaphore` + token-bucket backoff).
- Support batch inference (where the API supports it) for cost reduction.
- Add a CLI flag to emit JSON-only output for downstream programmatic consumers.

## Out of scope

- **Training a video-native model.** Different research project, different compute budget.
- **Real-time video processing.** The current pipeline is for offline analysis.
- **Production deployment.** This is a study, not a tool to ship.
