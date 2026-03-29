"""
Unit tests for SemanticVideoUnderstanding core logic.
Run with: pytest tests/
"""

import base64
import os
import sys

import pytest
from PIL import Image

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_diff_demo import (
    count_total_tokens,
    load_frames_from_input,
    load_images_in_order,
)
from vlm_client import VLMClient


# ---------------------------------------------------------------------------
# count_total_tokens
# ---------------------------------------------------------------------------

def test_count_tokens_empty_list():
    assert count_total_tokens([]) == 0


def test_count_tokens_returns_positive_int():
    texts = ["hello world", "this is a test sentence"]
    total = count_total_tokens(texts)
    assert isinstance(total, int)
    assert total > 0


def test_count_tokens_deterministic():
    texts = ["the quick brown fox jumps over the lazy dog"]
    assert count_total_tokens(texts) == count_total_tokens(texts)


def test_count_tokens_more_text_more_tokens():
    short = ["hi"]
    long = ["hi " * 100]
    assert count_total_tokens(long) > count_total_tokens(short)


def test_count_tokens_single_empty_string():
    # An empty string may tokenize to 0 or 1 depending on tokenizer; should not crash
    result = count_total_tokens([""])
    assert isinstance(result, int)
    assert result >= 0


# ---------------------------------------------------------------------------
# load_frames_from_input
# ---------------------------------------------------------------------------

def test_load_frames_invalid_path_raises():
    with pytest.raises(ValueError, match="does not exist"):
        load_frames_from_input("/nonexistent/path/that/does/not/exist")


def test_load_single_image(tmp_path):
    img = Image.new("RGB", (64, 64), color=(255, 0, 0))
    img_path = str(tmp_path / "test.jpg")
    img.save(img_path)

    frames = load_frames_from_input(img_path)
    assert len(frames) == 1
    assert isinstance(frames[0], Image.Image)


def test_load_images_from_folder(tmp_path):
    for i in range(3):
        img = Image.new("RGB", (64, 64), color=(i * 80, 0, 0))
        img.save(str(tmp_path / f"frame_{i:02d}.jpg"))

    frames = load_frames_from_input(str(tmp_path))
    assert len(frames) == 3


def test_load_images_folder_sorted_order(tmp_path):
    """Frames must be loaded in lexicographic (filename-sorted) order."""
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for i, color in enumerate(colors):
        img = Image.new("RGB", (64, 64), color=color)
        # Use PNG to avoid JPEG lossy compression altering pixel values
        img.save(str(tmp_path / f"frame_{i:02d}.png"))

    frames = load_frames_from_input(str(tmp_path))
    assert frames[0].getpixel((0, 0)) == (255, 0, 0)
    assert frames[1].getpixel((0, 0)) == (0, 255, 0)
    assert frames[2].getpixel((0, 0)) == (0, 0, 255)


def test_load_images_ignores_non_image_files(tmp_path):
    img = Image.new("RGB", (32, 32))
    img.save(str(tmp_path / "frame_00.png"))
    (tmp_path / "notes.txt").write_text("not an image")
    (tmp_path / "data.csv").write_text("a,b,c")

    frames = load_frames_from_input(str(tmp_path))
    assert len(frames) == 1


def test_load_images_empty_folder(tmp_path):
    frames = load_images_in_order(str(tmp_path))
    assert frames == []


# ---------------------------------------------------------------------------
# VLMClient
# ---------------------------------------------------------------------------

def test_vlm_client_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key"):
        VLMClient()


def test_vlm_client_raises_with_placeholder_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "your-api-key-here")
    with pytest.raises(ValueError, match="API key"):
        VLMClient()


def test_pil_to_base64_returns_valid_base64():
    img = Image.new("RGB", (64, 64), color=(128, 64, 32))
    result = VLMClient.pil_to_base64(img)

    assert isinstance(result, str)
    assert len(result) > 0
    # Must decode without error
    decoded = base64.b64decode(result)
    assert len(decoded) > 0


def test_pil_to_base64_different_images_differ():
    img1 = Image.new("RGB", (64, 64), color=(255, 0, 0))
    img2 = Image.new("RGB", (64, 64), color=(0, 0, 255))
    assert VLMClient.pil_to_base64(img1) != VLMClient.pil_to_base64(img2)


# ---------------------------------------------------------------------------
# Token reduction arithmetic (pure logic, no API)
# ---------------------------------------------------------------------------

def test_token_reduction_calculation():
    baseline, diff = 1000, 400
    reduction = baseline - diff
    pct = (reduction / baseline * 100) if baseline > 0 else 0.0
    assert reduction == 600
    assert abs(pct - 60.0) < 1e-9


def test_token_reduction_zero_baseline_no_division_error():
    baseline = 0
    pct = ((baseline - 0) / baseline * 100) if baseline > 0 else 0.0
    assert pct == 0.0


def test_token_reduction_diff_larger_than_baseline():
    baseline, diff = 100, 150
    reduction = baseline - diff
    pct = (reduction / baseline * 100) if baseline > 0 else 0.0
    assert reduction == -50
    assert abs(pct - (-50.0)) < 1e-9
