# 웹사이트를 크롤링하여 내용을 추출

import requests
from bs4 import BeautifulSoup

# 블로그 크롤링
def blog_crawling(url: str):
    """블로그 내용을 크롤링하는 함수

    블로그 링크를 입력하면 블로그 내용(블로그 전체 text)을 크롤링하여 반환함

    Args:
        url (str): 블로그 링크

    Returns:
        str: 블로그 내용(블로그 전체 text)
    """

    # 링크에 맞는 페이지 가져옴
    response = requests.get(url)
    # 페이지의 구성 코드(html)을 가져옴
    html = response.text
    # html 텍스트를 html 문법에 맞게 변경
    soup = BeautifulSoup(html, "html.parser")

    # html에서 ()안에 있는 선택자를 가져옴
    blogText = soup.select_one(".se-main-container").text

    return blogText
