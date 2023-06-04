from db import init
from logger import logger
from request import get_bond_and_store


def main():
    # init db
    init()
    # get bond list and store
    get_bond_and_store()


if __name__ == "__main__":
    main()
