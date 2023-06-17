import re
import requests
import tempfile
import textract
from logger import logger


def read_remote_document(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.log_error(
                f"read_remote_document - Get failed: {response.status_code}"
            )
            return

        file_suffix = url.split(".")[-1]
        with tempfile.NamedTemporaryFile(suffix=file_suffix) as temp:
            logger.log_info(f"document URL: {url}")
            temp.write(response.content)
            temp.seek(0)
            text_body = textract.process(temp.name, extension=file_suffix).decode(
                "utf-8"
            )

    except Exception as e:
        logger.log_warn(f"read_remote_document Exception: {e}")
        return ""

    text_body = re.sub(r"\n|-\s?\d+\s?-", "", text_body)
    # avoid NUL char
    text_body = text_body.replace("\x00", "")
    logger.log_info(f"text_body length: {len(text_body)}")
    return text_body


# def main():
#     # url = "http://static.sse.com.cn/bond/bridge/information/c/201803/d911f3949fdc42aca1cb5f625a8e7736.pdf"
#     url = "http://static.sse.com.cn/bond/bridge/information/c/201712/ccc538277f404e2e9e66ad26ab1d068e.doc"
#     text_body = read_remote_document(url)
#     print(text_body)


# main()
