import fitz
from docx import Document


def extract_text(file_path: str) -> str:

    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)

    if file_path.endswith(".docx"):
        return extract_docx_text(file_path)

    if file_path.endswith(".txt"):
        return extract_txt_text(file_path)

    raise Exception("Unsupported file type")


def extract_pdf_text(file_path: str) -> str:

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return clean_text(text)


def extract_docx_text(file_path: str) -> str:

    document = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    return clean_text(text)


def extract_txt_text(file_path: str) -> str:

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return clean_text(text)


def clean_text(text: str) -> str:

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    text = " ".join(text.split())

    return text