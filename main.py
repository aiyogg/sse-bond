from db import init, create_bond
from request import get_sse_bond_list


def main():
    # init db
    init()
    # get bond list
    bonds = get_sse_bond_list()
    print(bonds)
    # store bond list
    for bond in bonds:
        print(bond)
        create_bond(bond)


if __name__ == "__main__":
    main()
