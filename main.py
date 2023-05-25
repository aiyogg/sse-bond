import logging
import sys
from db import init, store_bond
from request import get_sse_bond_list
from logger import configure_logging

# set up logging
logging.basicConfig(level=logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console_handler)


def main():
    # configure logging
    configure_logging()
    # init db
    init()
    # get bond list
    bonds = get_sse_bond_list()
    if bonds is not None:
        # store bond list
        for bond in bonds:
            logging.debug(bond)
            store_bond(bond)


if __name__ == "__main__":
    main()
