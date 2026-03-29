import os
import time
import argparse
from typing import List, Optional
from PIL import Image
from vlm_client import VLMClient
from datetime import datetime

API_SLEEP_SECONDS: int = 3
DEFAULT_MAX_TOKENS: int = 200
DEFAULT_MODEL: str = "gpt-4o-mini"
DEFAULT_FRAME_INTERVAL: int = 1
DEFAULT_INPUT: str = "test_frame_diff"

BASELINE_PROMPT = "Describe this frame."
DIFF_PROMPT = (
    "You are given two consecutive frames from a video. "
    "Describe only what changed in the current frame compared to the previous one. "
    "Do not repeat objects, background, or attributes that stayed the same."
)

def extract_frames_from_video(video_path: str, max_frames: Optional[int] = None,
                              frame_interval: int = 1) -> List[Image.Image]:
    try:
        import cv2
    except ImportError:
        raise ImportError(
            "opencv-python is required for video processing. "
            "Install with: pip install opencv-python"
        )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frames = []
    frame_count = 0
    extracted_count = 0

    print(f"Extracting frames from video: {video_path}")
    if total_frames > 0:
        print(f"Total frames in video: {total_frames}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            frames.append(img)
            extracted_count += 1

            if max_frames and extracted_count >= max_frames:
                break

        frame_count += 1

    cap.release()
    print(f"Extracted {len(frames)} frames from video")
    return frames

def load_images_in_order(folder: str) -> List[Image.Image]:
    files = sorted(
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    imgs = []
    for f in files:
        path = os.path.join(folder, f)
        imgs.append(Image.open(path).convert("RGB"))
    print(f"Loaded {len(imgs)} frames from {folder}: {files}")
    return imgs

def load_frames_from_input(input_path: str, max_frames: Optional[int] = None,
                          frame_interval: int = 1) -> List[Image.Image]:
    if os.path.isfile(input_path):
        video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v")
        if input_path.lower().endswith(video_extensions):
            return extract_frames_from_video(input_path, max_frames, frame_interval)
        else:
            return [Image.open(input_path).convert("RGB")]
    elif os.path.isdir(input_path):
        return load_images_in_order(input_path)
    else:
        raise ValueError(f"Input path does not exist: {input_path}")

def run_baseline(vlm: VLMClient, images: List[Image.Image]) -> List[dict]:
    results = []
    for i, img in enumerate(images):
        text = vlm.describe_single(img, BASELINE_PROMPT)
        results.append({"frame_idx": i, "mode": "baseline", "text": text})
        time.sleep(API_SLEEP_SECONDS)
    return results

def run_diff(vlm: VLMClient, images: List[Image.Image]) -> List[dict]:
    results = []
    results.append({
        "frame_idx": 0,
        "mode": "diff",
        "text": "Initial frame. No previous frame to compare.",
    })
    for i in range(1, len(images)):
        prev_img = images[i - 1]
        curr_img = images[i]
        text = vlm.describe_pair(prev_img, curr_img, DIFF_PROMPT)
        results.append({"frame_idx": i, "mode": "diff", "text": text})
        time.sleep(API_SLEEP_SECONDS)
    return results

def pretty_print_compare(baseline: List[dict], diff: List[dict]) -> None:
    print("\n" + "=" * 55)
    print(" Baseline vs Semantic Diff Comparison")
    print("=" * 55)
    for b, d in zip(baseline, diff):
        idx = b["frame_idx"]
        print(f"\n[Frame {idx}]")
        print(f"  Baseline : {b['text']}")
        print(f"  Diff     : {d['text']}")
    print("=" * 55)

def count_total_tokens(texts: List[str], model_name: str = DEFAULT_MODEL) -> int:
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model_name)
        return sum(len(encoding.encode(t)) for t in texts)
    except ImportError:
        print("Warning: tiktoken not installed. Using GPT-2 tokenizer (less accurate).")
        print("Install with: pip install tiktoken")
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        return sum(len(tokenizer.encode(t)) for t in texts)

def save_results_to_file(baseline: List[dict], diff: List[dict], baseline_tokens: int, diff_tokens: int) -> None:
    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"outputs/results_{timestamp}.txt"

    with open(output_path, "w") as f:
        f.write("======= Baseline vs Diff (Semantic Diff Demo) =======\n\n")
        for b, d in zip(baseline, diff):
            idx = b["frame_idx"]
            f.write(f"[Frame {idx}]\n")
            f.write(f"Baseline: {b['text']}\n")
            f.write(f"Diff    : {d['text']}\n\n")

        f.write("======= Token Statistics =======\n")
        f.write(f"Total tokens (baseline): {baseline_tokens}\n")
        f.write(f"Total tokens (diff)    : {diff_tokens}\n")
        reduction = baseline_tokens - diff_tokens
        pct = (reduction / baseline_tokens * 100) if baseline_tokens > 0 else 0
        f.write(f"Token reduction        : {reduction} ({pct:.1f}%)\n")

    print(f"\nResults saved to: {output_path}\n")

def generate_token_plot(baseline_tokens: int, diff_tokens: int) -> None:
    """Save a bar chart comparing baseline vs. semantic diff token usage to plots/."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Warning: matplotlib not installed. Skipping plot. Install: pip install matplotlib")
        return

    os.makedirs("plots", exist_ok=True)

    labels = ["Baseline", "Semantic Diff"]
    counts = [baseline_tokens, diff_tokens]
    colors = ["#e06c75", "#61afef"]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, counts, color=colors, width=0.5)

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(counts) * 0.01,
            str(count),
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    reduction_pct = ((baseline_tokens - diff_tokens) / baseline_tokens * 100) if baseline_tokens > 0 else 0.0
    ax.set_title(f"Token Usage: Baseline vs Semantic Diff\n({reduction_pct:.1f}% reduction)", fontsize=12)
    ax.set_ylabel("Total Tokens")
    ax.set_ylim(0, max(counts) * 1.25 if counts else 1)

    plot_path = "plots/token_comparison.png"
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Plot saved to: {plot_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Semantic Diff Prompting for Video Understanding"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=DEFAULT_INPUT,
        help="Path to video file or folder containing images"
    )
    parser.add_argument("--max-frames", type=int, default=None)
    parser.add_argument("--frame-interval", type=int, default=DEFAULT_FRAME_INTERVAL)
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)

    args = parser.parse_args()

    vlm = VLMClient(model=args.model)
    images = load_frames_from_input(args.input, args.max_frames, args.frame_interval)

    if len(images) == 0:
        print("Error: No frames found!")
        return

    baseline_results = run_baseline(vlm, images)
    diff_results = run_diff(vlm, images)

    pretty_print_compare(baseline_results, diff_results)

    baseline_texts = [x["text"] for x in baseline_results]
    diff_texts = [x["text"] for x in diff_results]

    baseline_tokens = count_total_tokens(baseline_texts)
    diff_tokens = count_total_tokens(diff_texts)

    reduction = baseline_tokens - diff_tokens
    pct = (reduction / baseline_tokens * 100) if baseline_tokens > 0 else 0.0
    print("\n" + "=" * 40)
    print(" Token Statistics")
    print("=" * 40)
    print(f"  {'Metric':<22} {'Value':>10}")
    print(f"  {'-'*22} {'-'*10}")
    print(f"  {'Baseline tokens':<22} {baseline_tokens:>10}")
    print(f"  {'Semantic diff tokens':<22} {diff_tokens:>10}")
    print(f"  {'Reduction':<22} {reduction:>10}")
    print(f"  {'Reduction %':<22} {pct:>9.1f}%")
    print("=" * 40)

    save_results_to_file(baseline_results, diff_results, baseline_tokens, diff_tokens)
    generate_token_plot(baseline_tokens, diff_tokens)

if __name__ == "__main__":
    main()
