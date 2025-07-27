# tools/pdf_loader.py

from pdf2image import convert_from_path
from PIL import Image
import pytesseract

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a scanned or image-based PDF using OCR.
    Returns the concatenated text from all pages.
    """
    try:
        images = convert_from_path(pdf_path, dpi=300)
    except Exception as e:
        raise RuntimeError(f"PDF to image conversion failed: {e}")

    full_text = ""
    for i, img in enumerate(images):
        try:
            text = pytesseract.image_to_string(img)
            full_text += f"\n--- Page {i+1} ---\n{text.strip()}\n"
        except Exception as e:
            full_text += f"\n--- Page {i+1} ---\n[OCR Failed: {e}]\n"

    return full_text.strip()
