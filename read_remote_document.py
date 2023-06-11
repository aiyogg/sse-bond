import re
import requests
from logger import logger
from pypdf import PdfReader
import io
import magic
import textract


def read_remote_document(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.log_error(
                f"read_remote_document - Get failed: {response.status_code}"
            )
            return
        file_type = magic.from_buffer(response.content, mime=True)
        logger.log_info(f"file_type: {file_type}")
        file_type = "application/pdf"
        if file_type == "application/pdf":
            pdf_reader = PdfReader(io.BytesIO(response.content))
            page_count = pdf_reader.pages
            text_body = ""
            for page in page_count:
                text_body += page.extract_text()
        elif file_type == "application/msword":
            open("temp.doc", "wb").write(response.content)
            text_body = textract.process("temp.doc").decode("utf-8")

    except Exception as e:
        logger.log_error("read_remote_document Exception:", e)
        return

    text_body = re.sub(r"\n|-\s?\d+\s?-", " ", text_body)
    # avoid NUL char
    text_body = text_body.replace("\x00", "")
    logger.log_info(f"text_body length: {len(text_body)}")
    return text_body
