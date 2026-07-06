# SemanticVideoUnderstanding — Interview Talking Points

**Why hold the model fixed and vary the prompt.** The research question is prompt-engineering, not model selection. Comparing GPT-4o vs. Claude vs. Gemini at the same time as comparing baseline vs. diff would conflate two effects. By fixing the model, the diff effect is measured cleanly. The trade is that results don't generalize to other VLMs without a follow-up study — but that's a *next step*, not a confounded result.

**Why `tiktoken` matters more than people think.** The whole comparison hinges on token counts. Using a wrong-tokenizer measurement (counting whitespace-separated words, using a different model's tokenizer) would silently invalidate the experiment. `tiktoken` matches GPT-4's BPE exactly. Getting this detail right is the difference between a credible result and a meaningless one.

**Synthetic first-frame description.** Frame 0 in the diff pass returns the literal string `"Initial frame. No previous frame to compare."` instead of running the API. The reason isn't to save one API call — it's to give downstream code (output writer, bar chart, test assertions) a uniform per-frame structure. Skipping frame 0 would make the diff list one element shorter than the baseline list and cause off-by-one bugs in every consumer.

**No-network unit tests as a design principle.** 18 pytest cases, 0.5-second runtime, zero API calls, zero env-var requirements at test time. CI runs free, deterministic, and fast. The tests check the deterministic plumbing — token counting, frame loading, sort order, base64 encoding — exactly the places where bugs would silently invalidate the experiment. The non-deterministic parts (response parsing, retry) get integration tests with a real key, not unit tests.

**The honest experimental scope.** I measure what I can measure (token cost) on a sample I can run (subset of 141 videos) with the methodology I can defend (single model, fixed prompt phrasing, `tiktoken` measurement). I don't measure what I haven't measured (downstream-task utility, multi-model generality, prompt-sensitivity sweep, statistical confidence). The `limitations.md` doc spells out what's missing. Overclaiming a research result is worse than reporting a narrow but credible one.


