"""
read the remote PDF content
"""
import re
import requests
from logger import logger
from pypdf import PdfReader


def read_remote_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        logger.log_info(response.status_code)
        with open("temp.pdf", "wb") as file:
            file.write(response.content)
        pdf_file = open("temp.pdf", "rb")
        pdf_reader = PdfReader(pdf_file)

        page_count = pdf_reader.pages
        text_body = ""
        for page in page_count:
            text_body += page.extract_text()
    except Exception as e:
        logger.log_error("read_remote_pdf Exception:", e)
        return

    pdf_file.close()

    text_body = re.sub(r"\n|-\s?\d+\s?-", " ", text_body)
    return text_body
