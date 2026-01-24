#!/usr/bin/env python3
"""
Extract images from PDF files.
Extracts embedded images and rendered pages as images from PDF documents.
"""

import os
import sys
from pathlib import Path
import io

# Try to import required libraries
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Error: Pillow (PIL) is required. Install with: pip install pillow")
    sys.exit(1)

# Try to import PyMuPDF (preferred)
try:
    import fitz  # PyMuPDF
    USE_PYMUPDF = True
    USE_PDF2IMAGE = False
except ImportError:
    USE_PYMUPDF = False
    # Try pdf2image as alternative
    try:
        from pdf2image import convert_from_path
        USE_PDF2IMAGE = True
    except ImportError:
        USE_PDF2IMAGE = False
        print("Error: No PDF library found.")
        print("Install one of:")
        print("  - PyMuPDF: pip install PyMuPDF")
        print("  - pdf2image: pip install pdf2image (requires poppler)")
        sys.exit(1)


def extract_images_from_pdf_pymupdf(pdf_path: Path, output_dir: Path, pdf_name: str, extract_pages: bool, extract_embedded: bool):
    """Extract images using PyMuPDF."""
    doc = fitz.open(str(pdf_path))
    print(f"   Total pages: {len(doc)}")
    
    image_count = 0
    
    # Extract embedded images
    if extract_embedded:
        embedded_dir = output_dir / f"{pdf_name}_embedded"
        embedded_dir.mkdir(exist_ok=True)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Save embedded image
                image_filename = f"page_{page_num+1:03d}_img_{img_index+1:03d}.{image_ext}"
                image_path = embedded_dir / image_filename
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                image_count += 1
                print(f"   ✓ Extracted embedded image: {image_filename}")
    
    # Render pages as images
    if extract_pages:
        pages_dir = output_dir / f"{pdf_name}_pages"
        pages_dir.mkdir(exist_ok=True)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Render page as image (high resolution)
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Save page as image
            page_filename = f"page_{page_num+1:03d}.png"
            page_path = pages_dir / page_filename
            img.save(page_path, "PNG")
            
            print(f"   ✓ Rendered page {page_num+1}/{len(doc)}: {page_filename}")
    
    doc.close()
    print(f"\n✅ Completed: {image_count} embedded images extracted from {pdf_name}")
    if extract_pages:
        print(f"✅ Completed: {len(doc)} pages rendered as images from {pdf_name}")


def extract_images_from_pdf_pdf2image(pdf_path: Path, output_dir: Path, pdf_name: str, extract_pages: bool):
    """Extract images using pdf2image (only renders pages, doesn't extract embedded images)."""
    pages_dir = output_dir / f"{pdf_name}_pages"
    pages_dir.mkdir(exist_ok=True)
    
    print(f"   Rendering pages as images...")
    images = convert_from_path(str(pdf_path), dpi=200)  # 200 DPI for good quality
    
    for page_num, img in enumerate(images):
        page_filename = f"page_{page_num+1:03d}.png"
        page_path = pages_dir / page_filename
        img.save(page_path, "PNG")
        print(f"   ✓ Rendered page {page_num+1}/{len(images)}: {page_filename}")
    
    print(f"\n✅ Completed: {len(images)} pages rendered as images from {pdf_name}")
    print("   Note: pdf2image only renders pages, embedded images not extracted.")


def extract_images_from_pdf(pdf_path: str, output_dir: str, extract_pages: bool = True, extract_embedded: bool = True):
    """
    Extract images from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted images
        extract_pages: If True, render each page as an image
        extract_embedded: If True, extract embedded images from the PDF
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_name = pdf_path.stem
    print(f"\n📄 Processing: {pdf_path.name}")
    
    try:
        if USE_PYMUPDF:
            extract_images_from_pdf_pymupdf(pdf_path, output_dir, pdf_name, extract_pages, extract_embedded)
        elif USE_PDF2IMAGE:
            if extract_embedded:
                print("   ⚠️  Note: pdf2image cannot extract embedded images, only rendering pages.")
            extract_images_from_pdf_pdf2image(pdf_path, output_dir, pdf_name, extract_pages)
        
    except Exception as e:
        print(f"❌ Error processing {pdf_path.name}: {e}")
        import traceback
        traceback.print_exc()


def main():
    # PDF file paths
    presentation_pdf = "/Users/kaustubha/Library/Application Support/Cursor/User/workspaceStorage/546315c9f25c7cbbb1b3d586492d65f1/pdfs/b4723602-3065-48eb-84c6-2385bad6dbb2/presentation slides.pdf"
    proposal_pdf = "/Users/kaustubha/Library/Application Support/Cursor/User/workspaceStorage/546315c9f25c7cbbb1b3d586492d65f1/pdfs/799f11a1-cb25-4942-97c6-276c9e89cbd2/CS6180_Final_Report.pdf"
    
    # Output directory
    output_base = Path(__file__).parent / "extracted_images"
    
    print("=" * 60)
    print("PDF Image Extraction Tool")
    print("=" * 60)
    
    # Extract from presentation slides
    if os.path.exists(presentation_pdf):
        extract_images_from_pdf(
            presentation_pdf,
            output_base / "presentation",
            extract_pages=True,
            extract_embedded=True
        )
    else:
        print(f"⚠️  Presentation PDF not found: {presentation_pdf}")
    
    # Extract from project proposal
    if os.path.exists(proposal_pdf):
        extract_images_from_pdf(
            proposal_pdf,
            output_base / "proposal",
            extract_pages=True,
            extract_embedded=True
        )
    else:
        print(f"⚠️  Proposal PDF not found: {proposal_pdf}")
    
    print("\n" + "=" * 60)
    print(f"✅ All images extracted to: {output_base}")
    print("=" * 60)


if __name__ == "__main__":
    main()
