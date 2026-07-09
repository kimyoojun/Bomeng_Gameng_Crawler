# 웹사이트를 크롤링하여 내용을 추출

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 블로그 크롤링
def blog_crawling(url: str):
    """블로그 내용을 크롤링하는 함수

    블로그 링크를 입력하면 블로그 내용(블로그 전체 text)을 크롤링하여 반환함

    Args:
        url (str): 블로그 링크

    Returns:
        str: 블로그 내용(블로그 전체 text)
    """

    # HTTP 요청 해더: 간단한 브라우저 User-Agent 설정
    # (크롤러 차단을 줄이고 일부 사이트에서 정상적으로 응답을 받기 위함)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 블로그 URL에 GET 요청
    res = requests.get(url, headers=headers)

    # 응답 HTML을 BeautifulSoup으로 파싱
    # "html.parser"는 파이썬 내장 HTML 파서 사용
    soup = BeautifulSoup(res.text, "html.parser")

    # 현재 페이지 안에서 id가 mainFrame인 iframe을 찾음
    # 네이버 블로그는 바깥 페이지에 헤더/스킨을 두고
    # 실제 글 본문을 iframe(mainFrame) 안쪽 별도 페이지에 두는 경우가 많음
    iframe = soup.select_one("iframe#mainFrame")

    # mainFrame iframe이 존재한다면 -> 본문 페이지로 이동
    if iframe:
        # iframe의 src 속성이 실제 본문 url 상대 경로
        # urljoin을 사용하여 상대 경로를 절대 URL로 변경
        real_url = urljoin("https://blog.naver.com", iframe["src"])

        # 본문 페이지 URL로 다시 get 요청
        res = requests.get(real_url, headers=headers)

        # 새로 받은 본문 HTML을 다시 BeautifulSoup으로 파싱
        soup = BeautifulSoup(res.text, "html.parser")

    # 본문 전체를 감싸는 선택자 찾기
    container = soup.select_one("div.se-main-container").text.replace("\n", "")

    return container
