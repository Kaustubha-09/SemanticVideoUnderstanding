# Semantic Diff Prompting for Video Understanding

> **Final Project for CS6180: Generative AI**

A comparative study of baseline frame-by-frame video understanding versus semantic diff prompting, demonstrating significant token reduction while preserving temporal information.

---

## 📋 Overview

This project implements and compares two approaches to video understanding using vision language models:

- **Baseline Approach**: Each frame is described independently, leading to redundant information across frames
- **Semantic Diff Approach**: Only changes between consecutive frames are described, reducing token consumption while maintaining temporal dynamics

The semantic diff method can achieve substantial token savings (often 50-70% reduction) by avoiding repetition of static scene elements while preserving all dynamic information.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

### Installation

1. **Clone the repository** (or download the project files)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**

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

**Processing options:**
```bash
# Limit number of frames (useful for testing)
python semantic_diff_demo.py video.mp4 --max-frames 10

# Extract every Nth frame (reduce processing time for long videos)
python semantic_diff_demo.py video.mp4 --frame-interval 5

# Use a different OpenAI model
python semantic_diff_demo.py video.mp4 --model gpt-4o
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

---

## 📊 What the Script Does

1. **Extracts frames** from video (or loads images from folder/file)
2. **Runs baseline prompting** - describes each frame independently
3. **Runs semantic diff prompting** - describes only changes between consecutive frames
4. **Displays comparison** - side-by-side results in the terminal
5. **Calculates statistics** - token counts and reduction percentage
6. **Saves results** - timestamped file in `outputs/` directory

> **Note:** The script includes a 3-second delay between API calls to prevent rate limiting. Processing many frames may take some time.

---

## ⚙️ Command-Line Arguments

```
positional arguments:
  input                 Path to video file, image folder, or single image file
                       (default: test_frame_diff)

optional arguments:
  --max-frames MAX_FRAMES
                        Maximum number of frames to process from video
                        (default: all frames)
  
  --frame-interval FRAME_INTERVAL
                        Extract every Nth frame from video
                        (1 = all frames, 2 = every other frame, etc.)
                        (default: 1)
  
  --model MODEL         OpenAI model to use
                        Options: gpt-4o-mini, gpt-4o, gpt-4-vision-preview
                        (default: gpt-4o-mini)
```

---

## 📤 Output

### Console Output

The script displays:
- Frame extraction/loading progress
- Side-by-side comparison of baseline vs diff descriptions for each frame
- Token statistics:
  - Total tokens (baseline approach)
  - Total tokens (diff approach)
  - Token reduction amount and percentage

### Saved Results

Results are automatically saved to `outputs/results_YYYYMMDD_HHMMSS.txt` containing:
- Complete frame-by-frame comparison
- Token statistics
- Timestamp for tracking

---

## 🏗️ Project Structure

```
SemanticVideoUnderstanding/
├── semantic_diff_demo.py    # Main demo script
├── vlm_client.py            # Vision Language Model client wrapper
├── vision_test.py           # Simple image description test
├── requirements.txt         # Python dependencies
├── test_frame_diff/         # Sample test frames (4 PNG files)
├── test_img1.jpg           # Sample test image
├── test_videos/            # Sample video dataset
└── outputs/                # Results directory (auto-created)
```

### Key Files

- **`semantic_diff_demo.py`**: Main comparison script
  - Supports videos, image folders, and single images
  - Includes rate limiting and error handling
  - Saves timestamped results

- **`vlm_client.py`**: OpenAI API wrapper
  - Handles API calls with automatic retry on rate limits/errors
  - Supports single image and image pair descriptions
  - Base64 image encoding

- **`vision_test.py`**: Basic functionality test
  - Tests single image description

---

## 🔬 How It Works

### Baseline Approach

Each frame is described independently, leading to redundant information being repeated across frames.

**Example:** If a person is walking through a scene, their presence, the background, and scene elements are described in every frame.

### Semantic Diff Approach

Only changes between consecutive frames are described:

- **First frame**: Gets a full description (no previous frame to compare)
- **Subsequent frames**: Only describe what changed (movement, new objects, state changes)
- **Static elements**: Background and unchanged objects are not repeated
- **Result**: Significant token reduction while preserving temporal dynamics

### Example Comparison

**Baseline (Frame 2):**
> "A person is walking on a sidewalk. There are trees in the background. The sky is blue."

**Diff (Frame 2):**
> "The person has moved forward by two steps. Their right leg is now extended forward."

The diff approach focuses on the change, avoiding repetition of static scene elements, resulting in **50-70% token reduction** in typical scenarios.

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

If you encounter API key errors:
1. Verify the key is set: `echo $OPENAI_API_KEY`
2. Ensure the key starts with `sk-`
3. Check for extra spaces or quotes
4. Set it in the same terminal session where you run the script

### Rate Limiting

The script includes automatic retry logic with exponential backoff. If you still hit rate limits:
- Reduce the number of frames (`--max-frames`)
- Increase frame interval (`--frame-interval`)
- Use a model with higher rate limits (`--model gpt-4o`)

### Missing Dependencies

If you get import errors:
```bash
pip install -r requirements.txt
```

---

## 📝 License

This project is part of a course assignment for CS6180: Generative AI.

---

## 🙏 Acknowledgments

- OpenAI for the vision language model API
- Course instructors for project guidance
