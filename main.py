"""
main.py — Entry point for the Semantic Video Understanding project.

Usage:
    python main.py [input] [--max-frames N] [--frame-interval N] [--model MODEL]

Examples:
    python main.py test_frame_diff/
    python main.py video.mp4 --max-frames 10 --model gpt-4o
"""

from semantic_diff_demo import main

if __name__ == "__main__":
    main()
