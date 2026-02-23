from fastapi import FastAPI, File, UploadFile
from ai_parser import parse_po_text
import pdfplumber
import fitz  # PyMuPDF
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-po", tags=["PO AI AGENT"])
async def extract_po(file: UploadFile = File(...)):
    # Read uploaded PDF file
    pdf_bytes = await file.read()

    # Extract text from PDF using pdfplumber as primary method
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]

    # Fallback: Use PyMuPDF for pages with suspiciously little or no text
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for idx, page_text in enumerate(pages):
        # You may raise the threshold above 50 if needed
        if len(page_text.strip()) < 50:
            fitz_text = doc.load_page(idx).get_text()
            if len(fitz_text.strip()) > len(page_text.strip()):
                pages[idx] = fitz_text

    # Handle empty PDFs
    if not pages or not any(pages):
        return {"error": "No text extracted from PDF"}

    # First page text
    first_page_text = pages[0].strip()

    # Remaining pages text
    remaining_pages_text = "\n".join(p.strip() for p in pages[1:]) if len(pages) > 1 else ""

    # Parse with OpenAI
    parsed_json = parse_po_text(first_page_text, remaining_pages_text)

    return parsed_json
