from db import init, store_bond
from request import get_sse_bond_list
import logging

logging.getLogger("main").setLevel(logging.DEBUG)


def main():
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
