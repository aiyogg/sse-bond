import time
import schedule
from db import init, get_last_7days_bonds
from logger import logger
from request import get_bond_and_store
from constants import bond_field_name_map, audit_status_map
from send_email import send_email
from constants import email_style


def weekly_report():
    bonds = get_last_7days_bonds()
    logger.log_info(f"SQL: {bonds}")
    logger.log_info(f"Last 7 days total bonds: {len(bonds)}")
    if len(bonds) == 0:
        return
    ths = ""
    tdrows = []
    pick_fields = [
        "audit_name",
        "area",
        "plan_issue_amount",
        "company_name",
        "underwriter_short_name",
        "audit_status",
        "publish_date",
        "accept_date",
    ]
    for field in pick_fields:
        ths += f"<th>{bond_field_name_map[field]}</th>"
    for bond in bonds:
        tds = ""
        for field in pick_fields:
            td_content = ""
            if field == "audit_name":
                td_content = f'<a href="http://bond.sse.com.cn/bridge/information/index_detail.shtml?bound_id={getattr(bond, "bond_num")}" target="_blank">{getattr(bond, field)}</a>'
            elif field == "audit_status":
                td_content = f"{audit_status_map[getattr(bond, field)]}"
            else:
                td_content = getattr(bond, field)
            tds += f"<td>{td_content}</td>"
        tdrows.append(f"<tr>{tds}</tr>")
    table = (
        f"<table><thead><tr>{ths}</tr></thead><tbody>{''.join(tdrows)}</tbody></table>"
    )
    send_email(
        subject="Weekly SSE Bond Statistics",
        body=f"""\
            <html>
            <style>
            {email_style}
            </style>
            <body>
                <div class="container">
                    <h2 class="text-center">Here are the weekly statistics for SSE Bonds.</h2>
                    {table}
                </div>
            </body>
            </html>
        """,
        to_addr=["tengchenc@gmail.com"],
    )


def main():
    # init db
    init()
    get_bond_and_store()
    # weekly_report()


if __name__ == "__main__":
    main()

schedule.every().day.at("20:30").do(get_bond_and_store)
schedule.every().friday.at("20:30").do(weekly_report)

while True:
    schedule.run_pending()
    time.sleep(1)
