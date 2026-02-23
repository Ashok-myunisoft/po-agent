import fitz  # PyMuPDF
import os

def split_pdf_to_pages(pdf_path: str, output_dir: str):
    """
    Splits a PDF into individual single-page PDF files.
    """
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    file_list = []

    for page_num in range(len(doc)):
        single_pdf = fitz.open()
        single_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)

        page_path = os.path.join(output_dir, f"page_{page_num+1}.pdf")
        single_pdf.save(page_path)
        file_list.append(page_path)

    return file_list


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a single-page PDF file.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text.strip()
