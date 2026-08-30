import pymupdf


class PdfExtractionError(Exception):
    """Raised when a PDF cannot provide usable text."""


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract and combine selectable text from an in-memory PDF file."""
    if not pdf_bytes:
        raise PdfExtractionError("The uploaded resume file is empty.")

    try:
        document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except (pymupdf.FileDataError, RuntimeError, ValueError) as error:
        raise PdfExtractionError("The uploaded file is not a readable PDF.") from error

    try:
        text = "\n".join(page.get_text("text") for page in document).strip()
    finally:
        document.close()

    if len(text) < 20:
        raise PdfExtractionError(
            "No meaningful text could be extracted from this PDF. "
            "Please upload a text-based resume PDF."
        )

    return text
