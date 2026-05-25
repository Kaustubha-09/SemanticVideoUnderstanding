# Semantic Video Understanding — Portfolio Case Study

Final project for **CS 6180: Generative AI**, Northeastern University. Skim time: 3 minutes.

## The research question

Vision-language models (GPT-4o, Claude, Gemini) describe video frames one at a time. Most frames in a real video are *mostly the same as the previous frame* — the model is asked to redundantly re-describe static elements (background, fixed objects, lighting). Tokens are charged for the redundancy.

**Question:** if we ask the model to describe only *what changed* between consecutive frames, do we save tokens without losing temporal information?

## The experiment

A controlled comparison:

- Fixed model: GPT-4o (with `gpt-4o-mini` as the cheaper default).
- Two prompts: a baseline `"Describe this frame."` and a diff `"Describe only what changed in the current frame compared to the previous one."`
- Sample: 141 videos across 8 action categories (subset reported).
- Measurement: `tiktoken`-counted response tokens per frame, baseline vs. diff.

## The result

**50–70% token reduction** on non-first frames in the sample, without obvious loss of dynamic information (movements, new objects, state changes are all captured). First frame gets a synthetic `"Initial frame."` baseline so downstream consumers see a uniform shape.

## The engineering I'd defend in an interview

### 1. Holding the model fixed, varying the prompt

The research question is prompt-engineering, not model selection. Comparing GPT-4o vs. Claude vs. Gemini would conflate two effects. By holding the model fixed and varying only the prompt, the diff effect is measured cleanly. See [decisions.md, ADR-001](decisions.md#adr-001--prompt-comparison-not-model-comparison).

### 2. `tiktoken` for accurate measurement, GPT-2 fallback for portability

The whole comparison hinges on token counts. Using a wrong-tokenizer measurement would invalidate the result. `tiktoken` matches GPT-4's BPE exactly; GPT-2 fallback is for environments where `tiktoken` can't install. See [ADR-002](decisions.md#adr-002--tiktoken-as-the-primary-tokenizer-with-gpt-2-fallback).

### 3. Synthetic first-frame description for uniform shape

Frame 0 in the diff pass returns the literal string `"Initial frame. No previous frame to compare."` instead of running the API. Downstream code (output writer, bar chart, test assertions) sees a uniform per-frame structure. Skipping frame 0 would make the diff list shorter than the baseline list — pointless complexity for no payoff. See [ADR-003](decisions.md#adr-003--synthetic-first-frame-description).

### 4. 18 no-network unit tests for the deterministic parts

`tests/test_core.py` runs in under half a second, requires no API key, makes no network calls. Tests cover token counting, frame loading, sort order, API-key validation, base64 encoding, and token arithmetic — exactly the deterministic plumbing where silent bugs would invalidate the experiment. See [ADR-007](decisions.md#adr-007--no-network-tests).

### 5. Defaults tuned for the demo loop, not for production

`python main.py` with no args runs against `test_frame_diff/` (4 PNG frames) with `gpt-4o-mini` and produces a comparison in under a minute for under a cent of API spend. The README documents defensive recipes (`--max-frames 20 --frame-interval 10`) for real video inputs. See [ADR-006](decisions.md#adr-006--defaults-tuned-for-the-demo-loop-not-for-production).

## The honest part

- **Sample size is small.** 141 videos in 8 categories; subset reported. No CI bands, no held-out evaluation.
- **One model, one prompt phrasing.** Generalization to other models or other prompts is not proven.
- **Token cost is measured, downstream-task utility is not.** Token-efficient is not the same as task-useful. A real evaluation pairs both streams with a downstream task (summarization, video QA, action classification) and scores them.
- **No multi-frame context.** Each diff is computed against the immediately previous frame; longer-range temporal coherence is missed.

The full limitations list is in [docs/limitations.md](limitations.md). The roadmap to turn this from a study into a real benchmark is in [docs/roadmap.md](roadmap.md).

## What this signals to a recruiter

- I can frame a research question and design a controlled experiment to answer it.
- I write production-quality code for a research project: 18 deterministic unit tests, retry logic, configurable CLI, auto-saved artifacts.
- I know what my experiment proves vs. doesn't, and I document the gap explicitly — rather than overclaiming.
- I make defensible defaults (cheap model, small sample, capped frames) so anyone can reproduce the result without spending real money on API calls.
- I write ADRs even for a course project, because they're the cheapest way to make future-me understand past-me's choices.
