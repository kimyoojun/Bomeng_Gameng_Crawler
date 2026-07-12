from api.serper_api import search_api
from crawling import blog_crawling, official_crawling
from schemas.domain import blogs, officials
from api.openai_api import extract_tourist_spot
from excel import data_excel
from db.db_select import select_spot
from visit.jeju_crawling import visit_jeju_attractions

# 블로그를 크롤링한 데이터를 담는 변수
blogDatas = []

# 공식 사이트를 크롤링한 데이터를 담는 변수
officialDatas = []

# # 최종 관광지 데이터를 담는 변수
# travelData = []

# # 일부씩 관광지 데이터를 추가 하기 위해 만듬
# item = {}
# # 비짓제주 콘텐츠 id
# item["visit_id"] = ""
# # 관광지명
# item["name"] = ""
# # 관광지 타입 (축제, 관광지, 음식, 쇼핑, 숙박)
# item["spot_type"] = ""
# # 관광지 주소
# item["address"] = ""
# # 관광지 설명
# item["description"] = ""
# # 관광지 카테고리 (힐링, 엑티비티 등)
# item["categories"] = []
# # 누구랑 가기 좋은지(가족, 친구, 혼자 등)
# item["companions"] = []

# 최종 관광지 정보가 담길 리스트
attractionsDatas = visit_jeju_attractions()
# 순번을 넣기위한 변수
i = 0
# 가져온 관광지명 데이터 순회
for attractionsData in attractionsDatas:   
    i += 1

    # 순번 추가
    attractionsData["id"] = i

    # ()안에 검색어를 입력하여 나온 상위 10개의 페이지 링크를 담는 리스트
    pageLinks = search_api(attractionsData["region1cdLabel"] + " " + attractionsData["title"])

    # 페이지 리스트를 순환
    for link in pageLinks:

        # 링크가 블로그 링크인지 알아보기 위해 블로그 도메인 리스트 순환
        for blog in blogs:
            # 만약 블로그 도메인 리스트에 있는 도메인이 순환중인 링크 안에 포함되어 있을때
            if blog in link:
                # 해당 블로그 페이지의 내용을 크롤링
                data = blog_crawling(link, attractionsData["title"])
                # 블로그 데이터 리스트에 추가
                blogDatas.append(data)

        # 링크가 공식 사이트 링크인지 알아보기 위해 공식 사이트 도메인 리스트 순환
        for official in officials:

            # 만약 공식 사이트 도메인일때
            if official in link:
                # 해당 공식 사이트 페이지를 크롤링
                data = official_crawling(link, attractionsData["title"])
                # 공식사이트 데이터 리스트에 추가
                officialDatas.append(data)

    # 공식 사이트 데이터를 순환하며 원하는 형태의 데이터로 추출
    for officialData in officialDatas:

        # LLM을 사용하여 데이터 추출
        spotData = extract_tourist_spot(officialData)

        # if attractionsData["name"] == "":
        #     attractionsData["name"] = spotData.name
        
        # if attractionsData["address"] == "":
        #     attractionsData["address"] = spotData.address

        if attractionsData["description"] == "":
            attractionsData["description"] = spotData.description

    # 블로그 데이터를 순환하며 원하는 형태의 데이터로 추출
    for blogData in blogDatas:
        spotData = extract_tourist_spot(blogData)

        # 누구와 가기 좋은지 데이터가 비어있으면 추가
        if attractionsData["companions"] == []:
            attractionsData["companions"] = spotData.companions
        
        # 만약 비어있지 않으면 없는 데이터만 추가
        elif attractionsData["companions"]:
            # 추출한 데이터(spotData)중에서 저장한 데이터(attractionsData)에 없는 데이터만 추출하여 저장
            noCompanions = list(set(spotData.companions) - set(attractionsData["companions"]))

            # 추출한 데이터를 저장한 데이터(attractionsData)에 추가
            attractionsData["companions"].extend(noCompanions)

        # 관광지 카테고리 데이터 비어있으면 추가
        if attractionsData["categories"] == []:
            attractionsData["categories"] = spotData.categories

        # 비어있지 않을때 없는 데이터만 추가
        elif attractionsData["categories"]:

            # 관광지 카테고리 데이터의 존재하지 않는 카테고리만 추출
            noCategories = list(set(spotData.categories) - set(attractionsData["categories"]))

            # 추출한 데이터를 저장
            attractionsData["categories"].extend(noCategories)

# 데이터 엑셀로 저장
data_excel(attractionsDatas)
