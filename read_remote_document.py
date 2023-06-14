import re
import requests
import io
import magic
import PyPDF2
import docx
import tempfile
from logger import logger


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
        if file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
            page_count = len(pdf_reader.pages)
            text_body = ""
            for page in range(page_count):
                text_body += pdf_reader.pages[page].extract_text()
        elif file_type == "application/msword":
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
                f.write(response.content)
                doc = docx.Document(f.name)
                text_body = "\n".join([para.text for para in doc.paragraphs])

    except Exception as e:
        # logger.log_error("read_remote_document Exception:", e)
        return ""

    text_body = re.sub(r"\n|-\s?\d+\s?-", " ", text_body)
    # avoid NUL char
    text_body = text_body.replace("\x00", "")
    logger.log_info(f"text_body length: {len(text_body)}")
    return text_body


# def main():
#     # url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
#     # test docx
#     url = "http://static.sse.com.cn/bond/bridge/information/c/201606/49c5eefa735645699e367dc3c5a1424f.pdf"
#     text_body = read_remote_document(url)
#     print(text_body)


# main()
