from __future__ import division
import sys
import json
import requests
import traceback
import pprint
import pickle
from datetime import datetime
from multiprocessing import Pool, cpu_count

URL = "https://www.safekorea.go.kr/idsiSFK/bbs/user/selectBbsList.do"
HEADERS = {
    
}

def fetcher(page: int):
    req = requests.post(
        URL,
        headers=HEADERS,
        json={
            "bbs_searchInfo":{
                "pageIndex":page,  # pagination (starts from 1)
                "pageUnit":"100",  # posts per page
                "bbs_no":"63",
                "opCode":"",
                "search_type_v":"1",
                "search_val_v":"",
                "search_key_n":"",
                "search_start":"20160101",
                # "search_start": "20210512",
                "search_end": datetime.now().strftime("%Y%m%d")
            }
        }
    )

    data = req.json()
    pickle.dump(data, open("dumps/page-{}-{}.pkl".format(page, datetime.now().strftime("%Y%m%d-%H.%M.%S")), "wb"))
    return data


def fetchArticle(bbs_ordr: int):
    req = requests.post(
        "https://www.safekorea.go.kr/idsiSFK/bbs/user/selectBbsView.do",
        headers=HEADERS,
        json={
            "bbs_searchInfo":{
                "bbs_no": "63",
                "bbs_ordr": str(bbs_ordr)
            }
        }
    )

    return req.json(), bbs_ordr

"""
Response Structure
{
    "bbsList": [...posts],
    "rtnResult": {
        "pageSize": int,
        "resultCode": int,
        "resultMsg": str,
        "totCnt": int  # 전체 게시글 개수
    }
}

Post Structure (Example)
{'BBS_NO': 63,
 'BBS_ORDR': 102143,
 'BEGIN_DE': None,
 'BST_SNTNC_AT': None,
 'CFM_AT': None,
 'CFM_DT': None,
 'CFM_ID': None,
 'CMNT_CNT': None,
 'DELETE_AT': 'N',
 'DP': 1,
 'DSTR_INFO_QESTN_CL': None,
 'DSTR_TY_A_CD': None,
 'DSTR_TY_A_CD_NM': None,
 'DSTR_TY_B_CD': None,
 'DSTR_TY_B_CD_NM': None,
 'EDT_USE_AT': None,
 'ESTB_REFORM_CD': None,
 'ESTB_REFORM_NM': None,
 'FILE_CNT': None,
 'FRST_REGIST_DT': '2021-04-14',
 'HDLN': None,
 'IDX_NO': 81043,
 'KND_DE': None,
 'LAST_MODF_DT': '2021-04-14 17:10:49.0',
 'MEDIA_TY_CD': None,
 'MEDIA_TY_NM': None,
 'MODF_ID': None,
 'NOTICE_MATTER_AT': None,
 'NUM': 173,
 'PARNTS_NO': 0,
 'QRY_CNT': 0,
 'REPRSNT_IMAGE_DC': None,
 'REPRSNT_IMAGE_NM': None,
 'REPRSNT_IMAGE_WATER_LI_NM': None,
 'RGR_RGR_REFORM_DE': None,
 'ROWCNT': 3273,
 'SCRST_AT': None,
 'SJ': '2021/04/14 17:10:49 재난문자[남동구청]',
 'USR_DEPT_CD': None,
 'USR_DEPT_NM': None,
 'USR_EMAIL_ADRES': None,
 'USR_EMAIL_CD': None,
 'USR_EXPSR_AT': 'Y',
 'USR_ID': None,
 'USR_IP_ADRES': None,
 'USR_NATION_CD': None,
 'USR_NM': 'cbs',
 'USR_PASSWORD': None,
 'USR_TELNO': None}
"""


# data = req.json()
# posts = data['bbsList']

# pprint.pprint(data['bbsList'][0])
# print("[!] Fetched {:,} articles".format(len(posts)))
# pprint.pprint(data['rtnResult'])


if __name__ == "__main__":
    # BBS_ORDR, FRST_REGIST_DT, LAST_MODF_DT, NUM, SJ, USR_NM, CT
    data = dict()

    print("[!] Investigating post counts... ")
    max_page = int(fetcher(1)['rtnResult']['pageSize'])
    pages = list(range(1, max_page + 1))
    print("[!] Max page: {}".format(max_page))

    print("[!] Start fetching article numbers")
    started = datetime.now().timestamp()
    with Pool(cpu_count()) as p:
        for i, json_data in enumerate(p.imap_unordered(fetcher, pages), 1):
            for article in json_data["bbsList"]:
                data[str(article['BBS_ORDR'])] = [
                    article['FRST_REGIST_DT'],
                    article['LAST_MODF_DT'],
                    article['NUM'],
                    article['SJ'],
                    article['USR_NM'],
                    None
                ]

            elapsed = datetime.now().timestamp() - started
            jobs_per_second = i / elapsed
            estimated = (max_page - i) / jobs_per_second

            sys.stderr.write('\rdone {:%} [ELP {}:{}/EST {}:{}]'.format(
                i/max_page,
                int(elapsed // 60), int(elapsed % 60),
                int(estimated // 60), int(estimated % 60)
            ))

    print()
    print("[!] Fetched {:,} articles".format(len(data)))

    print("[!] Start fetching article contents")
    contentCnt = 0
    started = datetime.now().timestamp()
    with Pool(cpu_count()) as p:
        for i, (json_data, expected) in enumerate(p.imap_unordered(fetchArticle, data.keys()), 1):
            try:
                d = json_data['bbsMap']
                ordr = str(d['bbs_ordr'])
                content = d['cn']
                if ordr not in data:
                    print("[?] Unexpected ordr: {} (originally {})", ordr, expected)
                else:
                    data[ordr][-1] = content
            except KeyError:
                traceback.print_exc()
                print(json_data)
                exit(-1)

            elapsed = datetime.now().timestamp() - started
            jobs_per_second = i / elapsed
            estimated = (len(data) - i) / jobs_per_second

            sys.stderr.write('\rdone {:%} [ELP {}:{}/EST {}:{}]'.format(
                i/len(data),
                int(elapsed // 60), int(elapsed % 60),
                int(estimated // 60), int(estimated % 60)
            ))

    print()
    print("[!] Exporting")
    json.dump(data, open("articleMap.json", "w", encoding="UTF-8"))

    print("[!] Complete")
