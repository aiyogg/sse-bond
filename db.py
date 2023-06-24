import datetime
from typing import Literal
from peewee import *
from config import config
from logger import logger


database = PostgresqlDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database
        timezone = "Asia/Shanghai"


class Bond(BaseModel):
    modified_at = DateTimeField(default=datetime.datetime.now)
    audit_name = CharField(null=True)
    bond_num = CharField(null=True)
    bond_type = SmallIntegerField(null=True)
    area = CharField(null=True)
    company_name = CharField(null=True)
    company_code = CharField(null=True)
    plan_issue_amount = DecimalField(null=True)
    underwriter_name = CharField(null=True)
    underwriter_short_name = CharField(null=True)
    underwriter_code = CharField(null=True)
    audit_status = CharField(null=True)
    audit_sub_status = CharField(null=True)
    accept_date = CharField(null=True)
    csrc_code = CharField(null=True)
    reits_type = CharField(null=True)
    sec_name = CharField(null=True)
    publish_date = CharField(null=True)
    seq = CharField(null=True)
    prospectus_file = CharField(null=True)
    prospectus_file_path = CharField(null=True)
    prospectus_file_version = CharField(null=True)

    class Meta:
        table_name = "sse_bond"


class BondFeedback(BaseModel):
    bond_num = CharField(null=True)
    advice_id = CharField(null=True)
    type = CharField(null=True)
    upd_time = CharField(null=True)
    file_path = CharField(null=True)
    file_title = CharField(null=True)
    file_content = TextField(null=True)
    ai_summary = TextField(null=True)

    class Meta:
        table_name = "sse_bond_feedback"


def store_bond(bond) -> Literal["created", "updated", "skip"]:
    bond_num = bond["BOND_NUM"]
    defaults = {
        "audit_name": bond["AUDIT_NAME"],
        "bond_type": int(bond["BOND_TYPE"]),
        "area": bond["AREA"],
        "company_name": bond["LIST1"],
        "company_code": bond["LIST11"],
        "plan_issue_amount": float(bond["PLAN_ISSUE_AMOUNT"]),
        "underwriter_name": bond["LIST2"],
        "underwriter_short_name": bond["SHORT_NAME"],
        "underwriter_code": bond["LIST22"],
        "audit_status": bond["AUDIT_STATUS"],
        "audit_sub_status": bond["AUDIT_SUB_STATUS"],
        "accept_date": bond["ACCEPT_DATE"],
        "csrc_code": bond["CSRC_CODE"],
        "reits_type": bond["REITS_TYPE"],
        "sec_name": bond["SEC_NAME"],
        "publish_date": bond["PUBLISH_DATE"],
        "seq": bond["SEQ"],
        "prospectus_file": bond["PROSPECTUS_FILE"],
        "prospectus_file_path": bond["PROSPECTUS_FILE_PATH"],
        "prospectus_file_version": bond["PROSPECTUS_FILE_VERSION"],
    }
    stored_bond, created = Bond.get_or_create(bond_num=bond_num, defaults=defaults)
    if created:
        return "created"
    if stored_bond.seq == bond["SEQ"]:
        return "skip"
    Bond.update(modified_at=datetime.datetime.now(), **defaults).where(
        Bond.bond_num == bond_num
    ).execute()
    return "updated"


# get last 7 days bond list
def get_last_7days_bonds():
    return (
        Bond.select()
        # .where(Bond.publish_date == "2023-06-15")
        .where(
            Bond.publish_date
            >= (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
                "%Y-%m-%d"
            )
        )
        # .join(
        #     BondFeedback,
        #     JOIN.LEFT_OUTER,
        #     on=((Bond.bond_num == BondFeedback.bond_num)),
        # )
    )


def store_bond_feedback(bond_feedback) -> Literal["created", "updated"]:
    defaults = {
        "type": bond_feedback["TYPE"],
        "file_path": bond_feedback["FILE_PATH"],
        "file_title": bond_feedback["FILE_TITLE"],
        "file_content": bond_feedback["FILE_CONTENT"],
        "ai_summary": bond_feedback["AI_SUMMARY"],
    }
    stored_bond_feedback, created = BondFeedback.get_or_create(
        bond_num=bond_feedback["BOND_NUM"],
        advice_id=bond_feedback["ADVICE_ID"],
        upd_time=bond_feedback["UPD_TIME"],
        defaults=defaults,
    )
    if created:
        return "created"
    else:
        BondFeedback.update(**defaults).where(
            BondFeedback.bond_num == bond_feedback["BOND_NUM"],
            BondFeedback.advice_id == bond_feedback["ADVICE_ID"],
            BondFeedback.upd_time == bond_feedback["UPD_TIME"],
        ).execute()
    return "updated"


def init():
    database.init(
        str(config("db", "database")),
        user=config("db", "user"),
        password=config("db", "password"),
        host=config("db", "host"),
        port=config("db", "port"),
    )
    database.connect(True)
