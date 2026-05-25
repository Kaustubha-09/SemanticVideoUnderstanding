# Limitations

This is a course-project study. The honest scope is "two prompting strategies compared on a small sample".

## Sample size

- 141 videos in `test_videos/` across 8 action categories. The reported results are from a subset, not the full corpus.
- No statistical confidence intervals, no held-out test set, no cross-validation.
- The 50–70% token-reduction range is an observed empirical band, not a claim about the population mean.

## Single-model comparison

- One model: GPT-4o (with `gpt-4o-mini` as the cheaper default). No comparison across model families. The diff effect may not transfer to Claude, Gemini, or Llama vision models without re-measurement.

## Downstream-task evaluation missing

- We measure token *cost*, not task *utility*. The diff stream may be more token-efficient yet less useful for a downstream summarizer or video-QA agent. A real evaluation would measure both ends.

## No multi-frame context

- Each diff is computed against the immediately previous frame only. We don't pass a sliding window or temporal pooling. Long-range temporal coherence (e.g., a person re-entering frame after being off-screen) is missed.

## Prompt sensitivity

- The diff prompt is one specific phrasing. Different phrasings produce materially different outputs. We did not do a prompt-sensitivity sweep.

## API behavior is not deterministic

- GPT-4o is sampled with a temperature default that we did not fix. Re-running the same input produces slightly different descriptions. The token-count comparison is statistically meaningful only across multiple runs, which we did not perform at scale.

## Rate limiting is coarse

- `API_SLEEP_SECONDS = 3` is a fixed cooldown. Real adaptive rate-limit handling (exponential backoff with jitter, parallel-request batching) would be faster on bulk runs but is out of scope.

## No security review

- The OpenAI API key is read from `OPENAI_API_KEY` and used at call time. No key rotation, no usage caps from the app side (caps are imposed by OpenAI billing). Don't commit your key.

## Cost is bounded by frame count, not duration

- A 1-second 60fps clip with `--frame-interval 1` is 60 frames × 2 prompts = 120 API calls. A 60-second 1fps clip is 60 frames × 2 = 120 calls. Same cost. Long-form video at default settings is expensive; the README documents defensive recipes.

## Not a replacement for video LLMs

- Real video understanding models (VideoChat, Video-LLaMA, Gemini 1.5 Pro's native video input) ingest a video clip as a single multimodal input rather than as a sequence of independently described frames. This project's approach is *frame-level summarization with a token-cost lens*, not multimodal video reasoning. The two solve different problems.
