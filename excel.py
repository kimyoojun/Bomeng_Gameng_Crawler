# 데이터를 엑셀로 저장

import pandas as pd

columns = [
    "id",                 # 순번
    "title",              # 콘텐츠명
    "address",            # 주소                      
    "introduction",       # 간단소개 (visit jeju)
    "description",        # 관광지 소개(LLM)
    "companions",         # 누구랑 가기 좋은가?
    "categories",         # 카테고리
    "contentsId",         # 콘텐츠 ID
    "contentscdValue",    # 콘텐츠코드 값
    "contentsidLabel",    # 콘텐츠코드 라벨(또는 contentsId 라벨)
    "region1cdLabel",     # 1차 지역코드 라벨
    "region2cdLabel",     # 2차 지역코드 라벨
    "latitude",           # 위도
    "longitude",          # 경도
    "phoneno",            # 전화번호
    "imgPath",            # 일반 이미지 경로
    "thumbnailPath",      # 썸네일 이미지 경로
]

# 데이터를 엑셀로 저장하는 함수
def data_excel(data: list):
    df = pd.DataFrame(data, columns = columns)
    df.to_excel("jeju_spot.xlsx", index = False)
