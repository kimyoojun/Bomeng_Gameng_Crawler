from api.serper_api import search_api
from crawling import blog_crawling
from schemas.domain import blogs
from api.openai_api import extract_tourist_spot

# ()안에 검색어를 입력하여 나온 상위 10개의 페이지 링크를 담는 리스트
pageLinks = search_api("협재해수욕장")

# 블로그를 크롤링한 데이터를 담는 변수
blogDatas = []

# 관광지의 최종 데이터를 담는 변수
attractionsDatas = []

#  일부씩 관광지 데이터를 추가 하기 위해 만듬
item = {}
item["name"] = ""
item["companions"] = []
item["categories"] = []
item["address"] = ""
item["description"] = ""
item["spot_type"] = ""

# 페이지 리스트를 순환
for link in pageLinks:

    # 링크가 블로그 링크인지 알아보기 위해 블로그 도메인 리스트 순환
    for blog in blogs:
        # 만약 블로그 도메인 리스트에 있는 도메인이 순환중인 링크 안에 포함되어 있을때
        if blog in link:
            # 해당 블로그 페이지의 내용을 크롤링
            data = blog_crawling(link)
            # 블로그 데이터 리스트에 추가
            blogDatas.append(data)

for blogData in blogDatas:
    spotData = extract_tourist_spot(blogData)
    print(spotData)
    print("이름", spotData.name)
