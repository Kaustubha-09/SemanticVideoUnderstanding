# Architecture Decision Records

Dated decisions, append-only.

## ADR-001 · Prompt comparison, not model comparison

**Date:** 2025-03
**Status:** Accepted

We hold the model fixed (`gpt-4o-mini` default, `gpt-4o` available) and vary the prompt. We do not compare GPT-4o vs. Claude vs. Gemini.

**Why:** the research question is "does a diff prompt reduce token cost while preserving temporal information?" — that's a prompt-engineering question, not a model-selection question. Holding the model fixed lets the diff effect be measured cleanly.

**Cost:** results don't generalize to other VLMs without a follow-up study.

---

## ADR-002 · `tiktoken` as the primary tokenizer with GPT-2 fallback

**Date:** 2025-03
**Status:** Accepted

`tiktoken` matches GPT-4's BPE tokenizer exactly. GPT-2 tokenizer is the fallback when `tiktoken` is unavailable.

**Why:** the comparison's whole point is token counts; using a tokenizer that doesn't match the inference model would invalidate the measurement. GPT-2 fallback is rough but better than nothing — useful in offline test environments that can't install `tiktoken`.

---

## ADR-003 · Synthetic first-frame description

**Date:** 2025-03
**Status:** Accepted

For the diff pass, frame 0 returns the literal string `"Initial frame. No previous frame to compare."` instead of running the API call.

**Why:** downstream consumers (the output writer, the bar chart, the test assertions) expect a uniform per-frame structure. Skipping frame 0 would make the diff list one shorter than the baseline list, which complicates everything for no payoff.

**Cost:** the diff "token count" for frame 0 is the tokenization of this fixed sentence — a fair zero baseline for the actual API token cost.

---

## ADR-004 · `API_SLEEP_SECONDS = 3` cooldown

**Date:** 2025-03
**Status:** Accepted

Between consecutive API calls, the client sleeps for 3 seconds.

**Why:** coarse but reliable. The free-tier OpenAI rate limit is generous but not infinite; a 30-frame baseline run would otherwise burst 30 requests in under a second and risk a 429. Three seconds smooths the request rate without making the demo painfully slow.

**Cost:** a 10-frame run takes ~30 seconds instead of ~1 second. Acceptable for a demo; would be replaced by adaptive backoff in a real tool.

---

## ADR-005 · OpenCV for video, PIL for folders

**Date:** 2025-03
**Status:** Accepted

Video → `cv2.VideoCapture`. Folder → `PIL.Image.open` sorted lexicographically.

**Why:** OpenCV is the industry standard for video frame I/O and handles every container format we care about (mp4, mov, mkv, webm). PIL handles still images more cleanly than OpenCV (no BGR↔RGB conversion needed) and integrates directly with the base64 encoder.

**Cost:** two image libraries. Mitigated by `cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` + `PIL.Image.fromarray` at the seam — every frame becomes a `PIL.Image` before it leaves the loader.

---

## ADR-006 · Defaults tuned for the demo loop, not for production

**Date:** 2025-03
**Status:** Accepted

- Default input: `test_frame_diff/` (4 PNG frames).
- Default model: `gpt-4o-mini` (cheap).
- Default `--max-frames`: no cap.
- Default `--frame-interval`: 1.

**Why:** `python main.py` with no args should produce a useful comparison in under a minute and under one cent of API spend. Defaults that surprise you with a $5 invoice are a bad demo experience.

**For real videos:** the README documents the defensive recipe — `--max-frames 20 --frame-interval 10` keeps cost bounded on long inputs.

---

## ADR-007 · No-network tests

**Date:** 2025-03
**Status:** Accepted

The 18 pytest cases in `tests/test_core.py` make zero API calls and read no env vars at test time (a placeholder `sk-test-placeholder` is passed when the loader needs *some* key).

**Why:** CI runs in 0.5 seconds, doesn't require an API key as a secret, doesn't fail on network outage, doesn't cost money. The tests check the deterministic parts of the pipeline (token counting, frame loading, sort order, base64 encoding) — exactly the parts where bugs would silently invalidate the experiment.

**What's not tested:** the actual API request shape, the response parsing, the retry behavior. These need an integration test with a real key — out of scope for the demo CI.
