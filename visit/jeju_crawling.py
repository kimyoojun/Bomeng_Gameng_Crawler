# 비짓제주 크롤링

import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

attractionsData = []

# visit_jeju api key
apiKey = os.environ.get("VISIT_JEJU_API_KEY")

# 비짓제주에서 관광지와 세부 정보를 추출하는 함수
def visit_jeju_attractions():
    """visit jeju api를 사용하여 관광지와 세부 정보 추출

    Args:
        None

    return:
        list: 관광지 세부 정보
    """

    # 관광지 코드 category=c1
    # 전체 페이지를 확인하기 위한 api 호출
    pageRes = requests.get(f"http://api.visitjeju.net/vsjApi/contents/searchList?apiKey={apiKey}&category=c1&locale=kr") 
    # json 형태로 변경
    pageData = pageRes.json()
    # 전체 페이지수 저장
    pageCount = pageData["pageCount"]

    # 전체 페이지 만큼 페이지 반복
    for i in range(1, pageCount + 1):
        # 관광지 코드 category=c1
        res = requests.get(f"http://api.visitjeju.net/vsjApi/contents/searchList?apiKey={apiKey}&locale=kr&category=c1&page={i}") 

        data = res.json()

        # item 딕셔너리 저장
        items = data["items"]

        # 딕셔너리 수 만큼 반복
        for item in items:
            # 콘텐츠 ID
            contentsId = item.get("contentsid")
            # 콘텐츠코드 값
            contentscdValue = item.get("contentscd").get("value")
            # 콘텐츠코드 라벨
            contentsidLabel = item.get("contentscd").get("label")
            # 콘텐츠명
            title = item.get("title")
            # 1차 지역코드 라벨
            region1cdLabel = item.get("region1cd").get("label")
            # 2차 지역코드 라벨
            region2cdLabel = item.get("region2cd").get("label")
            # 주소
            address = item.get("address")
            # 간단소개
            introduction = item.get("introduction")
            # 위도
            latitude = item.get("latitude")
            # 경도
            longitude = item.get("longitude")
            # 전화번호
            phoneno = item.get("phoneno")
            
            if item.get("repPhoto"):
                # 일반 이미지 경로
                imgPath = item.get("repPhoto").get("photoid").get("imgpath")
                # 썸네일 이미지경로
                thumbnailPath = item.get("repPhoto").get("photoid").get("thumbnailpath")

            # 딕셔너리 생성
            place = {
                # 콘텐츠 ID
                "contentsId" : contentsId,
                # 콘텐츠코드 값
                "contentscdValue" : contentscdValue,
                # 콘텐츠코드 라벨
                "contentsidLabel" : contentsidLabel,
                # 콘텐츠명
                "title" : title,
                # 1차 지역코드 라벨
                "region1cdLabel" : region1cdLabel,
                # 2차 지역코드 라벨
                "region2cdLabel" : region2cdLabel,
                # 주소
                "address" : address,
                # 간단소개 (visit jeju)
                "introduction" : introduction,
                # 관광지 소개(LLM)
                "description" : "",
                # 누구랑 가기 좋은가?
                "companions" : "",
                # 카테고리
                "categories" : "",
                # 위도
                "latitude" : latitude,
                # 경도
                "longitude" : longitude,
                # 전화번호
                "phoneno" : phoneno,
                # 일반 이미지 경로
                "imgPath" : imgPath,
                # 썸네일 이미지경로
                "thumbnailPath" : thumbnailPath,
            }

            # 딕셔너리를 리스트에 추가
            attractionsData.append(place)

    return attractionsData

# columns = [
#     "contentsId",         # 콘텐츠 ID
#     "contentscdValue",    # 콘텐츠코드 값
#     "contentsidLabel",    # 콘텐츠코드 라벨(또는 contentsId 라벨)
#     "title",              # 콘텐츠명
#     "region1cdLabel",     # 1차 지역코드 라벨
#     "region2cdLabel",     # 2차 지역코드 라벨
#     "address",            # 주소
#     "introduction",       # 간단소개
#     "latitude",           # 위도
#     "longitude",          # 경도
#     "phoneno",            # 전화번호
#     "imgPath",            # 일반 이미지 경로
#     "thumbnailPath",      # 썸네일 이미지 경로
# ]

# df = pd.DataFrame(attractionsData, columns = columns)
# df.to_excel("visit_jeju_spot.xlsx", index = False)
