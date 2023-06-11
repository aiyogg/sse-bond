import requests
import json
import re
from logger import logger
from db import store_bond, store_bond_feedback
from read_remote_document import read_remote_document
from config import SSE_BOND_STATIC_URL


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
    # logger.log_info(f"result: {data}, params: {params}")
    return data


def get_sse_bond_list():
    # set referer header
    headers = {"Referer": "http://bond.sse.com.cn/"}
    # set request params
    params = {
        "isPagination": "false",
        # "isPagination": "true",
        "bond_type": "0",
        "sqlId": "COMMON_SSE_ZCZZQXMLB",
        # "status": "2",
        # "pageHelp.pageSize": "1",
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


def get_bond_and_store():
    # get bond list
    bonds = get_sse_bond_list()
    if bonds is not None:
        # store bond list
        for bond in bonds:
            logger.log_info(
                f"债券名称: %s {bond['AUDIT_NAME']}",
            )
            rfs = get_sse_bond_reference(bond["BOND_NUM"])
            if rfs is not None and len(rfs) > 0:
                logger.log_info(
                    f"募集说明书: %s {rfs[0]['FILE_TITLE']}",
                )
                # assign field to bond
                bond["PROSPECTUS_FILE"] = rfs[0]["FILE_TITLE"]
                bond["PROSPECTUS_FILE_PATH"] = rfs[0]["FILE_PATH"]
                bond["PROSPECTUS_FILE_VERSION"] = rfs[0]["FILE_VERSION"]
            if store_bond(bond):
                logger.log_info("已存在，无更新!")
                continue
            fbs = get_sse_bond_feedback(bond["BOND_NUM"])
            if fbs is not None and len(fbs) > 0:
                for fb in fbs:
                    logger.log_info(
                        f"反馈意见及回复: %s {fb['FILE_TITLE']}",
                    )
                    pdf_url = SSE_BOND_STATIC_URL + fb["FILE_PATH"]
                    pdf_text = read_remote_document(pdf_url)
                    logger.log_info(len(pdf_text))
                    fb["BOND_NUM"] = bond["BOND_NUM"]
                    fb["FILE_CONTENT"] = pdf_text
                    fb["AI_SUMMARY"] = ""
                    store_bond_feedback(fb)
