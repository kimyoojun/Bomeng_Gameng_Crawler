# 관광지를 검색하여 페이지 링크를 반환

import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

serper_key = os.environ.get("SERPER_API_KEY")

url = "https://google.serper.dev/search"

headers = {
    "X-API-KEY": serper_key,
    "Content-Type": "application/json"
}

def search_api(region: str):
    """검색 결과 상위 10개 사이트 링크들을 반환하는 함수

    Args:
        region (str): 검색할 검색어

    Returns:
        list: 검색결과 상위 10개 사이트 링크
    """
    payload = {
        # 검색어
        "q": "협재 해수욕장",
        # 나라
        "gl": "kr",
        # 언어
        "hl": "ko",
        # 날짜
        # "tbs": "qdr:h"
    }

    response = requests.request("POST" ,url, headers=headers, json=payload)

    # json 형식의 문자열을 파이썬 객체로 변경
    pages = json.loads(response.text)

    # 서치 결과 페이지 링크를 담을 리스트
    pageLinks = []

    # 서치 결과 리스트를 반복문으로 링크만 리스트에 저장
    for page in pages["organic"]:
        pageLinks.append(page["link"])

    return pageLinks
