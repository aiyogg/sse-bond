"""
read the remote PDF content
"""
import requests
from logger import Logger
from pypdf import PdfReader

logger = Logger("error.log")


def read_remote_pdf(pdf_url):
    parts = []

    def visitor_body(text, cm, tm, font_dict, font_size):
        y = tm[5]
        if y > 53:
            parts.append(text.replace("\n", ""))

    try:
        response = requests.get(pdf_url)
        logger.log_info(response.status_code)
        with open("temp.pdf", "wb") as file:
            file.write(response.content)
        pdf_file = open("temp.pdf", "rb")
        pdf_reader = PdfReader(pdf_file)
    except Exception as e:
        logger.log_error(e)
        return
    page_count = pdf_reader.pages
    for page in page_count:
        page.extract_text(visitor_text=visitor_body)

    text_body = "".join(parts)
    return text_body
