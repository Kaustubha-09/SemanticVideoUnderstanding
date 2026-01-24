# Semantic Diff Prompting for Video Understanding

> **Final Project for CS6180: Generative AI**

A comparative study of baseline frame-by-frame video understanding versus semantic diff prompting, demonstrating significant token reduction while preserving temporal information.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)](https://openai.com/)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Features](#-features)
- [Project Structure](#️-project-structure)
- [Requirements](#-requirements)
- [Troubleshooting](#-troubleshooting)

---

## 📋 Overview

This project implements and compares two approaches to video understanding using vision language models:

- **Baseline Approach**: Each frame is described independently, leading to redundant information across frames
- **Semantic Diff Approach**: Only changes between consecutive frames are described, reducing token consumption while maintaining temporal dynamics

> **📹 Demo Video**: Try the project with the presentation slides video. Place your video in `demo_videos/` and run:
> ```bash
> python semantic_diff_demo.py demo_videos/presentation_slides.mp4
> ```

### Key Benefits

- 🎯 **Token Efficiency**: Achieves 50-70% token reduction compared to baseline methods
- ⚡ **Cost Savings**: Lower API costs due to reduced token usage
- 🔍 **Temporal Focus**: Captures dynamic changes while ignoring static elements
- 📊 **Comprehensive Comparison**: Side-by-side analysis of both approaches
- 💾 **Persistent Results**: Automatic saving of comparisons and statistics

The semantic diff method achieves substantial token savings by avoiding repetition of static scene elements while preserving all dynamic information.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

### Installation

1. **Clone the repository** (or download the project files)
   ```bash
   git clone <repository-url>
   cd SemanticVideoUnderstanding
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key:**

   **macOS/Linux:**
   ```bash
   export OPENAI_API_KEY="sk-your-actual-api-key-here"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:OPENAI_API_KEY="sk-your-actual-api-key-here"
   ```

   **Verify the key is set:**
   ```bash
   echo $OPENAI_API_KEY  # macOS/Linux
   echo %OPENAI_API_KEY% # Windows CMD
   ```

   > **Note:** If using a virtual environment or conda, set the API key in the same terminal session where you'll run the scripts.

4. **Run the demo:**
   ```bash
   python semantic_diff_demo.py
   ```

---

## 💻 Usage

### Main Demo: Semantic Diff Comparison

The `semantic_diff_demo.py` script supports multiple input types: video files, image folders, or single image files.

#### Video Files

```bash
python semantic_diff_demo.py path/to/your/video.mp4
```

**Supported formats:** `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.webm`, `.m4v`

**Examples:**

```bash
# Process a video file
python semantic_diff_demo.py "/path/to/video.mp4"

# Process presentation slides video (place video in demo_videos/ first)
python semantic_diff_demo.py demo_videos/presentation_slides.mp4

# Or use absolute path if video is elsewhere
python semantic_diff_demo.py "/path/to/presentation slides.mp4"

# Quick test with limited frames
python semantic_diff_demo.py video.mp4 --max-frames 10

# Process every 5th frame (useful for long videos)
python semantic_diff_demo.py video.mp4 --frame-interval 5

# Use a different OpenAI model
python semantic_diff_demo.py video.mp4 --model gpt-4o

# Combine options: process every 3rd frame, max 20 frames
python semantic_diff_demo.py video.mp4 --frame-interval 3 --max-frames 20
```

#### Image Folders

```bash
python semantic_diff_demo.py path/to/image/folder
```

**Default test folder:**
```bash
python semantic_diff_demo.py                    # Uses test_frame_diff/
python semantic_diff_demo.py test_frame_diff    # Explicit
```

#### Single Image Files

```bash
python semantic_diff_demo.py path/to/image.jpg
```

### Simple Vision Test

Test basic image description functionality:

```bash
python vision_test.py
```

This processes `test_img1.jpg` with the vision model.

### How It Works

The script processes videos/images through these steps:

1. **Extracts frames** from video (or loads images from folder/file)
2. **Runs baseline prompting** - describes each frame independently
3. **Runs semantic diff prompting** - describes only changes between consecutive frames
4. **Displays comparison** - side-by-side results in the terminal
5. **Calculates statistics** - token counts and reduction percentage
6. **Saves results** - timestamped file in `outputs/` directory

> **Note:** The script includes a 3-second delay between API calls to prevent rate limiting. Processing many frames may take some time.

#### Command-Line Arguments

**Positional Arguments:**

| Argument | Description | Default |
|----------|-------------|---------|
| `input` | Path to video file, image folder, or single image file | `test_frame_diff` |

**Optional Arguments:**

| Flag | Description | Default | Example |
|------|-------------|---------|---------|
| `--max-frames` | Maximum number of frames to process | All frames | `--max-frames 10` |
| `--frame-interval` | Extract every Nth frame (1=all, 2=every other, etc.) | `1` | `--frame-interval 5` |
| `--model` | OpenAI model to use | `gpt-4o-mini` | `--model gpt-4o` |

**Available Models:**
- `gpt-4o-mini` (default) - Cost-effective, good performance
- `gpt-4o` - Higher quality, higher cost
- `gpt-4-vision-preview` - Legacy vision model

#### Output

The script displays progress and side-by-side comparisons in the terminal, then saves results to `outputs/results_YYYYMMDD_HHMMSS.txt` with complete frame-by-frame comparisons and token statistics.

---

## 🏗️ Project Structure

```
SemanticVideoUnderstanding/
├── semantic_diff_demo.py    # Main demo script - compares baseline vs diff
├── vlm_client.py            # Vision Language Model client wrapper
├── vision_test.py           # Simple image description test
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── Project_Proposal.pdf     # Original project proposal
├── docs/                    # Documentation and diagrams
│   └── images/             # Visual diagrams and examples
│       ├── traditional_challenges.png
│       ├── semantic_diff_concept.png
│       ├── semantic_diff_output.png
│       └── processing_pipeline.png
│
├── test_frame_diff/         # Sample test frames (4 PNG files)
│   ├── diff_test_01.png
│   ├── diff_test_02.png
│   ├── diff_test_03.png
│   └── diff_test_04.png
│
├── test_img1.jpg           # Sample test image
│
├── demo_videos/            # Demo videos (e.g., presentation slides)
│   └── presentation_slides.mp4  # Place demo videos here
│
├── test_videos/            # Sample video dataset (organized by action)
│   ├── Bending something so that it deforms/
│   ├── closing something/
│   ├── Folding something/
│   ├── Pouring something into something/
│   └── ... (more action categories)
│
└── outputs/                # Results directory (auto-created)
    └── results_YYYYMMDD_HHMMSS.txt
```

### Key Files

#### `semantic_diff_demo.py`
Main comparison script that:
- Extracts frames from videos or loads images from folders/files
- Runs baseline prompting (independent frame descriptions)
- Runs semantic diff prompting (change-only descriptions)
- Compares results side-by-side
- Calculates token statistics and reduction percentages
- Saves timestamped results to `outputs/` directory
- Includes rate limiting (3-second delays) and error handling

#### `vlm_client.py`
OpenAI API wrapper that:
- Handles API calls with automatic retry on rate limits/errors
- Supports single image descriptions (`describe_single`)
- Supports image pair descriptions (`describe_pair`)
- Base64 image encoding for API transmission
- Exponential backoff retry logic

#### `vision_test.py`
Basic functionality test:
- Tests single image description capability
- Uses `test_img1.jpg` as input
- Useful for verifying API setup

---

## 🔬 How It Works

### Baseline Approach

Each frame is described independently, leading to redundant information being repeated across frames.

**Example:** If a person is walking through a scene, their presence, the background, and scene elements are described in every frame.

![Traditional Video Captioning Challenges](docs/images/traditional_challenges.png)

*Traditional frame-by-frame captioning can lead to hallucinations and redundant descriptions, as shown in the diagram above.*

### Semantic Diff Approach

Only changes between consecutive frames are described:

- **First frame**: Gets a full description (no previous frame to compare)
- **Subsequent frames**: Only describe what changed (movement, new objects, state changes)
- **Static elements**: Background and unchanged objects are not repeated
- **Result**: Significant token reduction while preserving temporal dynamics

![Semantic Diff Prompting: Core Concept](docs/images/semantic_diff_concept.png)

*The semantic diff approach compares consecutive frames and describes only the changes, avoiding repetition of static elements and preventing hallucinations.*

### Example Comparison

Consider a video of a person walking through a scene:

**Frame 1 (Baseline):**
> "A person is walking on a sidewalk. There are trees in the background. The sky is blue."

**Frame 1 (Diff):**
> "Initial frame. No previous frame to compare."

**Frame 2 (Baseline):**
> "A person is walking on a sidewalk. There are trees in the background. The sky is blue."

**Frame 2 (Diff):**
> "The person has moved forward by two steps. Their right leg is now extended forward."

**Frame 3 (Baseline):**
> "A person is walking on a sidewalk. There are trees in the background. The sky is blue."

**Frame 3 (Diff):**
> "The person continues walking. Left leg now extended forward."

**Analysis:**
- **Baseline**: Repeats static elements (sidewalk, trees, sky) in every frame → **High token count**
- **Diff**: Only describes changes (movement) → **50-70% token reduction**

The diff approach focuses on temporal changes, avoiding repetition of static scene elements while preserving all dynamic information.

![Semantic Diff Output Example](docs/images/semantic_diff_output.png)

*Real example output showing how semantic diff descriptions focus on changes (pasta removal, hand appearance, flour addition) while baseline descriptions repeat static scene elements.*

---

## ✨ Features

- ✅ **Multiple input formats**: Video files, image folders, single images
- ✅ **Flexible frame sampling**: Max frames limit, frame interval selection
- ✅ **Robust error handling**: Automatic retry on rate limits and API errors
- ✅ **Accurate token counting**: Uses GPT-4 tokenizer (tiktoken) for precise counts
- ✅ **Persistent results**: Timestamped output files for easy tracking
- ✅ **Rate limiting**: Built-in delays to prevent API throttling
- ✅ **Comprehensive statistics**: Token reduction metrics and percentages

---

## 📦 Requirements

- **Python**: 3.7 or higher
- **OpenAI API Key**: Required for vision language model access
- **Dependencies** (see `requirements.txt`):
  - `openai>=1.0.0`
  - `pillow>=10.0.0`
  - `transformers>=4.30.0`
  - `tiktoken>=0.5.0`
  - `opencv-python>=4.8.0`

---

## 🔧 Troubleshooting

### API Key Issues

**Problem:** `OpenAI API key not found` or authentication errors

**Solutions:**
1. Verify the key is set:
   ```bash
   echo $OPENAI_API_KEY  # macOS/Linux
   echo %OPENAI_API_KEY% # Windows CMD
   ```
2. Ensure the key starts with `sk-`
3. Check for extra spaces or quotes around the key
4. Set it in the same terminal session where you run the script
5. If using a virtual environment, activate it before setting the key

### Rate Limiting

**Problem:** `Rate limit hit` or `429 Too Many Requests` errors

**Solutions:**
- The script includes automatic retry logic with exponential backoff
- Reduce the number of frames: `--max-frames 5`
- Increase frame interval: `--frame-interval 10`
- Use a model with higher rate limits: `--model gpt-4o`
- Wait a few minutes and retry

### Missing Dependencies

**Problem:** `ModuleNotFoundError` or import errors

**Solutions:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install openai pillow transformers tiktoken opencv-python
```

### Video Processing Issues

**Problem:** `Could not open video file` or video codec errors

**Solutions:**
- Ensure the video file exists and path is correct
- Check video format is supported (`.mp4`, `.avi`, `.mov`, `.webm`, etc.)
- Install/update OpenCV: `pip install --upgrade opencv-python`
- Try converting the video to MP4 format

### Memory Issues

**Problem:** Out of memory when processing large videos

**Solutions:**
- Use `--max-frames` to limit processing
- Use `--frame-interval` to skip frames
- Process shorter video segments
- Close other applications to free memory

---

## 🎓 Use Cases & Performance

This project is useful for video summarization, action recognition, cost optimization, research, and content analysis.

**Typical Performance:**
- **Token Reduction**: 50-70% compared to baseline
- **Cost Savings**: Proportional to token reduction
- **Accuracy**: Maintains temporal information while reducing redundancy
- **Processing Time**: Similar to baseline (API call overhead is the same)

## 🔬 Methodology

![Overall Processing Pipeline](docs/images/processing_pipeline.png)

*The complete processing pipeline showing both baseline and diff-prompting paths, with evaluation and final results.*

The methodology follows these steps: frame extraction, baseline processing (independent descriptions), diff processing (change-only descriptions), token counting with tiktoken, comparison generation, and result persistence.

## 📝 License

This project is part of a course assignment for CS6180: Generative AI.

---

## 🙏 Acknowledgments

- **OpenAI** for providing the vision language model API (GPT-4o, GPT-4o-mini)
- **Course Instructors** for project guidance and feedback
- **Open Source Community** for the excellent libraries used in this project

---

## 📮 Contact & Contributions

**Author:** Kaustubha V E

- 📧 **Email**: [kaustubha.ev@gmail.com](mailto:kaustubha.ev@gmail.com)
- 🌐 **Portfolio**: [kaustubha-09.github.io](https://kaustubha-09.github.io)
- 💼 **LinkedIn**: [linkedin.com/in/kaustubha-ve](https://linkedin.com/in/kaustubha-ve)

For questions, issues, or contributions related to this project, feel free to reach out!

**Note:** This is an academic project. For production use, consider additional optimizations, error handling, and scalability improvements.
