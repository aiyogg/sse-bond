from peewee import *
from config import config

database = PostgresqlDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class Bond(BaseModel):
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

    class Meta:
        table_name = "sse_bond"


def create_bond(bond):
    Bond.create(
        audit_name=bond["AUDIT_NAME"],
        bond_num=bond["BOND_NUM"],
        bond_type=int(bond["BOND_TYPE"]),
        area=bond["AREA"],
        company_name=bond["LIST1"],
        company_code=bond["LIST11"],
        plan_issue_amount=float(bond["PLAN_ISSUE_AMOUNT"]),
        underwriter_name=bond["LIST2"],
        underwriter_short_name=bond["SHORT_NAME"],
        underwriter_code=bond["LIST22"],
        audit_status=bond["AUDIT_STATUS"],
        audit_sub_status=bond["AUDIT_SUB_STATUS"],
        accept_date=bond["ACCEPT_DATE"],
        csrc_code=bond["CSRC_CODE"],
        reits_type=bond["REITS_TYPE"],
        sec_name=bond["SEC_NAME"],
        publish_date=bond["PUBLISH_DATE"],
        seq=bond["SEQ"],
    )


def init():
    database.init(
        str(config("db", "database")),
        user=config("db", "user"),
        password=config("db", "password"),
        host=config("db", "host"),
        port=config("db", "port"),
    )
    database.connect(True)
