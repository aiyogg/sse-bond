import logging
from db import init, store_bond
from request import get_sse_bond_list, get_sse_bond_feedback
from logger import Logger
from config import SSE_BOND_STATIC_URL
from read_remote_pdf import read_remote_pdf

logger = Logger("error.log")


def main():
    # init db
    init()

    refs = get_sse_bond_feedback("23829")
    logger.log_info(refs)
    if refs is not None and len(refs) > 0:
        pdf_url = SSE_BOND_STATIC_URL + refs[0]["FILE_PATH"]
        logger.log_info(pdf_url)
        read_remote_pdf(pdf_url)
    # get bond list
    # bonds = get_sse_bond_list()
    # if bonds is not None:
    #     # store bond list
    #     logging.debug(len(bonds))
    # for bond in bonds:
    # store_bond(bond)


if __name__ == "__main__":
    main()
