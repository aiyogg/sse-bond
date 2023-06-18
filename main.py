from db import init, get_last_7days_bonds
from logger import logger
from request import get_bond_and_store
import time

import schedule


def main():
    # init db
    init()
    bonds = get_last_7days_bonds()
    logger.log_info(f"Total bonds: {len(bonds)}")
    for bond in bonds:
        logger.log_info(bond.publish_date)
    # get bond list and store
    # get_bond_and_store()


if __name__ == "__main__":
    main()

schedule.every().day.at("10:30").do(get_bond_and_store)

while True:
    schedule.run_pending()
    time.sleep(1)
