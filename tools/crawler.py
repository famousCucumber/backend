from bs4 import BeautifulSoup
import sys
import requests
import json
from datetime import datetime, timedelta
from finder import get_keyword


def get_bbs_ordr_list(last_ordr):
    current_date = datetime.now().strftime('%Y%m%d')
    last_date = datetime.now() - timedelta(days=29)
    last_date = last_date.strftime('%Y%m%d')

    current_page = 0
    stop = False
    result = []
    url = "https://www.safekorea.go.kr/idsiSFK/bbs/user/selectBbsList.do"

    while not stop:
        current_page += 1

        # Request data
        data = f'''
            {{
                "bbs_searchInfo": {{
                    "pageIndex":"{current_page}",
                    "pageUnit":"100",
                    "pageSize":"100",
                    "firstIndex":"1",
                    "lastIndex":"1",
                    "recordCountPerPage":"10",
                    "bbs_no":"63",
                    "bbs_ordr":"",
                    "use":"",
                    "opCode":"",
                    "search_type_v":"",
                    "search_val_v":"",
                    "search_key_n":"",
                    "search_notice":"",
                    "search_use":"",
                    "search_permits":"",
                    "search_disaster_a":"",
                    "search_disaster_b":"",
                    "search_amendment":"",
                    "search_start":"{last_date}",
                    "search_end":"{current_date}",
                    "search_date_limit":"{last_date}"
                }}
            }}
            '''

        # Request
        response = requests.post(url, data)

        # Response
        json_data = json.loads(response.content.decode("utf-8"))
        bbs_list = json_data["bbsList"]

        # If empty page
        if len(bbs_list) == 0:
            stop = True
            continue

        # Result
        for bbs in bbs_list:
            ordr = int(bbs["BBS_ORDR"])
            if ordr <= last_ordr:
                stop = True
                continue

            result.append(ordr)

    return result


def get_article_list(ordr_list):
    result = []
    url = "https://www.safekorea.go.kr/idsiSFK/bbs/user/selectBbsView.do"

    for ordr in ordr_list:
        # Request data
        data = f'''
            {{
                "bbs_searchInfo": {{
                    "pageIndex":"1",
                    "pageUnit":"10",
                    "pageSize":"10",
                    "firstIndex":"1",
                    "lastIndex":"1",
                    "recordCountPerPage":"10",
                    "bbs_no":"63",
                    "bbs_ordr":"{ordr}",
                    "use":"",
                    "opCode":"2",
                    "search_type_v":"",
                    "search_val_v":"",
                    "search_key_n":"",
                    "search_notice":"",
                    "search_use":"",
                    "search_permits":"",
                    "search_disaster_a":"",
                    "search_disaster_b":"",
                    "search_amendment":"",
                    "search_start":"",
                    "search_end":""
                }}
            }}
        '''

        # Request
        response = requests.post(url, data)

        # Response
        json_data = json.loads(response.content.decode("utf-8"))

        # Check empty article
        result_code = int(json_data["rtnResult"]["resultCode"])
        if result_code < 0:
            continue

        # Append article map to result(list)
        bbs_map = json_data["bbsMap"]
        dt = bbs_map["sj"][:19]
        cn = bbs_map["cn"]
        article_map = {
            "ordr": ordr,
            "date": dt,
            "content": cn
        }

        result.append(article_map)

    return result


if __name__ == "__main__":
    last_ordr = int(sys.argv[1])
    ordr_list = get_bbs_ordr_list(last_ordr)
    article_list = get_article_list(ordr_list)
    results = []
    for article in article_list:
        obj = article
        keyword = get_keyword(article["content"])
        for key in keyword:
            obj[key] = keyword[key]
        results.append(obj)
    print(results)