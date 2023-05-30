# 上交所债券文档爬取

import requests
import json
import re
from logger import logger


# common request func
def doRequest(headers, params):
    url = "http://query.sse.com.cn/commonQuery.do"
    params["jsonCallBack"] = "jsonpCallback666"
    with requests.Session() as session:
        response = session.get(url, headers=headers, params=params)
    response.encoding = "utf-8"
    # deal with jsonp response
    data = response.text
    # remove jsonp callback
    data = re.sub(r"^jsonpCallback666\(|\)$", "", data)

    # to json
    data = json.loads(data)
    # get `result` from dict object
    if data["result"] is None:
        logger.log_error("no result")
        return
    data = data["result"]
    return data


def get_sse_bond_list():
    # set referer header
    headers = {"Referer": "http://bond.sse.com.cn/"}
    # set request params
    params = {
        "isPagination": "true",
        # "isPagination": "false",
        "pageHelp.pageSize": "1",
        "bond_type": "0",
        # 'status': '2',
        "sqlId": "COMMON_SSE_ZCZZQXMLB",
    }
    return doRequest(headers, params)


def get_sse_bond_reference(audit_id):
    headers = {"Referer": "http://bond.sse.com.cn/"}
    params = {
        "isPagination": "false",
        "sqlId": "COMMON_SSE_ZCZZQXMXXXX_XXPLWJ_ZGSMS",
        "audit_id": audit_id,
    }
    return doRequest(headers, params)


def get_sse_bond_feedback(audit_id):
    # set referer header
    headers = {"Referer": "http://bond.sse.com.cn/"}
    # set request params
    params = {
        "isPagination": "false",
        "sqlId": "COMMON_SSE_ZCZZQXMXXXX_FKXX_ALL",
        "audit_id": audit_id,
    }

    return doRequest(headers, params)


# get bond and its feedback
def get_bond_and_feedback():
    result = []
    feedback = []
    list = get_sse_bond_list()
    if list is None:
        return
    for bond in list:
        audit_id = bond["BOND_NUM"]
        reference_files = get_sse_bond_reference(audit_id)
        # number can compare with number string?
        if int(bond["AUDIT_STATUS"]) > 1:
            feedback = get_sse_bond_feedback(audit_id)

        result.append(
            {
                "bond": bond,
                "feedback": feedback if feedback is not None else [],
                "reference_file": reference_files[0]
                if reference_files is not None
                else [],
            }
        )

    print(json.dumps(result, indent=4, ensure_ascii=False))
    # save result as json file
    with open("sse_bond.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))


# get_bond_and_feedback()
