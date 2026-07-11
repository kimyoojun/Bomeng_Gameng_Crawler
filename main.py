from api.serper_api import search_api
from crawling import blog_crawling, official_crawling
from schemas.domain import blogs, officials
from api.openai_api import extract_tourist_spot

# ()안에 검색어를 입력하여 나온 상위 10개의 페이지 링크를 담는 리스트
pageLinks = search_api("협재해수욕장")

# 블로그를 크롤링한 데이터를 담는 변수
blogDatas = []

# 공식 사이트를 크롤링한 데이터를 담는 변수
officialDatas = []

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

    # 링크가 공식 사이트 링크인지 알아보기 위해 공식 사이트 도메인 리스트 순환
    for official in officials:

        # 만약 공식 사이트 도메인일때
        if official in link:
            # 해당 공식 사이트 페이지를 크롤링
            data = official_crawling(link)
            # 공식사이트 데이터 리스트에 추가
            officialDatas.append(data)

# 공식 사이트 데이터를 순환하며 원하는 형태의 데이터로 추출
for officialData in officialDatas:

    # LLM을 사용하여 데이터 추출
    spotData = extract_tourist_spot(officialData)

    if item["name"] == "":
        item["name"] = spotData.name
    
    if item["address"] == "":
        item["address"] = spotData.address

    if item["description"] == "":
        item["description"] = spotData.description

# 블로그 데이터를 순환하며 원하는 형태의 데이터로 추출
for blogData in blogDatas:
    spotData = extract_tourist_spot(blogData)

    # 누구와 가기 좋은지 데이터가 비어있으면 추가
    if item["companions"] == []:
        item["companions"] = spotData.companions
    
    # 만약 비어있지 않으면 없는 데이터만 추가
    elif item["companions"]:
        # 추출한 데이터(spotData)중에서 저장한 데이터(item)에 없는 데이터만 추출하여 저장
        noCompanions = list(set(spotData.companions) - set(item["companions"]))

        # 추출한 데이터를 저장한 데이터(item)에 추가
        item["companions"].extend(noCompanions)

    if item["categories"] == []:
        item["categories"] = spotData.categories

    elif item["categories"]:

        noCategories = list(set(spotData.categories) - set(item["categories"]))

        item["categories"].extend(noCategories)

print(item)