# href="//static.sse.com.cn/bond/bridge/information/c/202303/917b7ac761c64019b7fdd867481bb461.pdf"
SSE_BOND_STATIC_URL = "http://static.sse.com.cn/bond"
# bond detail web page url
SSE_BOND_DETAIL_URL = (
    "http://bond.sse.com.cn/bridge/information/index_detail.shtml?bound_id="
)


bond_type_map = {
    0: "小公募",
    1: "私募",
    2: "资产支持证券(ABS)",
    3: "大公募",
}


audit_status_map = {
    "0": "已申报",
    "1": "已受理",
    "2": "已反馈",
    "3": "已接收反馈意见",
    "4": "通过",
    "5": "未通过",
    "8": "终止",
    "9": "中止",
    "10": "已回复交易所意见",
    "11": "提交注册",
    "12": "注册生效",
}


bond_field_name_map = {
    "bond_num": "债券ID",
    "audit_name": "债券名称",
    "bond_type": "债券类型",
    "area": "地区",
    "company_name": "发行人",
    "company_code": "发行人代码",
    "plan_issue_amount": "拟发行金额(亿元)",
    "underwriter_name": "承销商/管理人",
    "underwriter_short_name": "承销商/管理人简称",
    "underwriter_code": "承销商/管理人代码",
    "audit_status": "项目状态",
    "audit_sub_status": "项目子状态",
    "accept_date": "受理日期",
    "csrc_code": "证监会行业",
    "reits_type": "REITs类型",
    "sec_name": "证券简称",
    "publish_date": "更新日期",
    "seq": "序列",
    "prospectus_file": "募集说明书",
    "prospectus_file_path": "招股说明书路径",
}


email_style = """\
    body {
        margin: 0;
        font-family: "Microsoft YaHei", "微软雅黑", "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 16px;
        line-height: 1.5;
        color: #333;
        background-color: #f5f5f5;
    }
    .container {
        max-width: 1200px;
        margin: 50px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .text-center {
        text-align: center;
    }
    .emphasize {
        font-weight: bold;
        font-size: 18px;
    }
    .safe {
        color: green;
    }
    .danger {
        color: red;
    }
    .warning {
        color: orange;
    }
    table {
        border-collapse: collapse;
        border: 1px solid rgb(200, 200, 200);
        letter-spacing: 1px;
        font-family: sans-serif;
        font-size: 0.8rem;
    }
    td,
    th {
        border: 1px solid rgb(190, 190, 190);
        padding: 10px;
        text-align: center;
    }
    tr:nth-child(even) {
        background-color: #eee;
    }
"""
