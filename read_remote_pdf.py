"""
read the remote PDF content
"""
import requests
import logging
from pypdf import PdfReader


def read_remote_pdf(pdf_url):
    parts = []

    def visitor_body(text, cm, tm, font_dict, font_size):
        y = tm[5]
        if y > 53:
            parts.append(text.replace("\n", ""))

    try:
        response = requests.get(pdf_url)
        with open("temp.pdf", "wb") as file:
            file.write(response.content)
        pdf_file = open("temp.pdf", "rb")
        pdf_reader = PdfReader(pdf_file)
    except Exception as e:
        logging.error(e)
        return
    page_count = pdf_reader.pages
    for page in page_count:
        page.extract_text(visitor_text=visitor_body)

    text_body = "".join(parts)
    return text_body
