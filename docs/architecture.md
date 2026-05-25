# Architecture

A study-by-construction comparing two prompting strategies for vision-language models on video frames: the *baseline* (describe each frame independently) versus the *semantic diff* (describe only what changed between consecutive frames).

## Pipeline

```
                ┌─────────────────────────────────────┐
                │       Input (one of three)          │
                │  - Video file (.mp4 / .mov / .webm) │
                │  - Image folder (.jpg / .png)       │
                │  - Single image                     │
                └────────────────┬────────────────────┘
                                 │
                                 ▼
                ┌─────────────────────────────────────┐
                │   load_frames_from_input()          │
                │  ├─ Video → OpenCV VideoCapture     │
                │  │   sample every Nth frame         │
                │  │   max_frames cap                 │
                │  └─ Folder → PIL Image.open sorted  │
                └────────────────┬────────────────────┘
                                 │
                  ┌──────────────┴──────────────┐
                  ▼                             ▼
        ┌──────────────────┐         ┌──────────────────────┐
        │  Baseline pass   │         │  Semantic-diff pass  │
        │  for each frame: │         │  for frame ≥ 1:      │
        │  GPT-4o(         │         │  GPT-4o(             │
        │    "Describe     │         │    [prev, current],  │
        │     this frame." │         │    DIFF_PROMPT)      │
        │  )               │         │  frame 0: "Initial   │
        │                  │         │   frame." (no prev)  │
        └────────┬─────────┘         └─────────┬────────────┘
                 │                             │
                 ▼                             ▼
        ┌──────────────────────────────────────────────┐
        │  tiktoken token count per response           │
        │  Sum, average, % reduction                   │
        └──────────────────────┬───────────────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │  Outputs                                     │
        │  ├─ stdout: side-by-side table               │
        │  ├─ outputs/results_<ts>.txt                 │
        │  └─ plots/token_comparison.png (matplotlib)  │
        └──────────────────────────────────────────────┘
```

## Prompt design

```python
BASELINE_PROMPT = "Describe this frame."

DIFF_PROMPT = (
    "You are given two consecutive frames from a video. "
    "Describe only what changed in the current frame compared to the previous one. "
    "Do not repeat objects, background, or attributes that stayed the same."
)
```

The diff prompt is one paragraph, no role-play, no chain-of-thought scaffolding. The instruction *not to repeat* is the load-bearing phrase — without it, GPT-4o defaults to re-describing the scene.

The first frame of any sequence gets `"Initial frame. No previous frame to compare."` as a synthetic baseline so downstream code sees a uniform shape.

## API client

`vlm_client.py` wraps the OpenAI client with:

- **Exponential backoff retry** on rate-limit errors (429).
- **Base64 image encoding** for the multimodal chat-completion payload.
- **`API_SLEEP_SECONDS = 3`** cooldown between calls — coarse but effective for staying under per-minute limits on the demo run.
- **Configurable model** (`gpt-4o-mini` default, `gpt-4o` and `gpt-4-vision-preview` supported).
- **`DEFAULT_MAX_TOKENS = 200`** on response cap.

## Token counting

`tiktoken` with the GPT-4 tokenizer is the primary measurement; a GPT-2 tokenizer fallback handles environments where `tiktoken` is unavailable. Reported numbers in the comparison table are computed over the response text only — the prompt text and image token contribution are not counted (the comparison is fair because both strategies share the same prompt structure).

## Frame sampling

Two knobs control cost:

- `--max-frames N` — hard cap on total frames processed.
- `--frame-interval N` — extract every Nth frame.

Defaults to "no cap" plus "every frame" — fine for short test videos, expensive on a 30 s 30 fps clip (900 frames × 2 prompts). The README shows defensive recipes (`--max-frames 5 --frame-interval 10`) for long-input runs.

## Outputs

| Where | Format | Purpose |
|---|---|---|
| stdout | aligned table | per-frame baseline-vs-diff side by side, token stats |
| `outputs/results_YYYYMMDD_HHMMSS.txt` | plain text | full comparison preserved for later analysis |
| `plots/token_comparison.png` | matplotlib bar | per-frame token counts, baseline vs diff |

Both `outputs/` and `plots/` are auto-created at first run if missing.

## Tests

`tests/test_core.py` — 18 tests, no network, no API key. Coverage:

- `count_tokens()` — known fixed strings, empty string, multi-byte
- Frame loader — empty folder, file extension filtering, sort order
- API key reader — missing env var, valid prefix, malformed
- Base64 encoder — round-trip, file-not-found, empty file
- Token arithmetic — sum, average, percentage delta

The full test loop runs in under half a second.

## What the experiment proves (and doesn't)

**Proves:**
- On the sample videos in `test_videos/`, the diff prompt produces 50–70% fewer tokens than baseline per non-first frame.
- The diff captures real change information — movement, new objects, state transitions — without hallucinating differences that aren't there (verified by spot-checking on small clips).

**Does not prove:**
- Generalization beyond the small sample. The action dataset is 141 videos across 8 categories; we ran on a subset.
- Downstream-task quality. Token-efficient is not the same as task-useful — a real evaluation would measure how well a downstream summarizer or QA agent performs on the diff stream versus the baseline stream.
- Multi-frame coherence. Each frame's diff is computed independently against its predecessor; we don't model longer temporal context.

These are honest experimental limits, not a knock on the approach. The point of the project was to *measure*, not to claim a production tool.
