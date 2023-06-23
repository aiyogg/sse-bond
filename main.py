import time
from db import init, get_last_7days_bonds
from logger import logger
from request import get_bond_and_store
from constants import bond_field_name_map

import schedule


def main():
    # init db
    init()
    bonds = get_last_7days_bonds()
    logger.log_info(f"Total bonds: {len(bonds)}")
    for bond in bonds:
        # list all field with mapping
        for field in bond_field_name_map:
            logger.log_info(f"{bond_field_name_map[field]}: {getattr(bond, field)}")

    # get bond list and store
    get_bond_and_store()


if __name__ == "__main__":
    main()

schedule.every().day.at("21:30").do(get_bond_and_store)

while True:
    schedule.run_pending()
    time.sleep(1)
