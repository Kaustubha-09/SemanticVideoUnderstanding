# PDF Image Extraction

This script extracts images from PDF files (presentation slides and project proposal).

## Setup

Install the required dependencies:

```bash
pip install PyMuPDF pillow
```

Or if you prefer using pdf2image:

```bash
pip install pdf2image pillow
# On macOS, also install poppler: brew install poppler
```

## Usage

Simply run:

```bash
python3 extract_pdf_images.py
```

The script will:
1. Extract images from the presentation slides PDF
2. Extract images from the project proposal PDF
3. Save all images to `extracted_images/` directory

## Output Structure

```
extracted_images/
├── presentation/
│   ├── presentation slides_pages/      # Rendered pages as PNG images
│   └── presentation slides_embedded/   # Embedded images from PDF
└── proposal/
    ├── CS6180_Final_Report_pages/      # Rendered pages as PNG images
    └── CS6180_Final_Report_embedded/   # Embedded images from PDF
```

## Features

- **Page Rendering**: Converts each PDF page to a high-resolution PNG image
- **Embedded Image Extraction**: Extracts images embedded within the PDF
- **Organized Output**: Separates images by source PDF and type
- **High Quality**: Uses 2x zoom (PyMuPDF) or 200 DPI (pdf2image) for crisp images
