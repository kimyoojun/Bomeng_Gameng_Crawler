from typing import List, Optional
from pydantic import BaseModel, Field

class TouristSpotExtract(BaseModel):
    name: str = Field(description="관광지명")
    companions: List[str] = Field(
        default_factory=list,
        description="누구랑 가기 좋은지 (예: 가족, 커플, 친구, 혼자)"
    )
    categories: List[str] = Field(
        default_factory=list,
        description="카테고리 (힐링, 자연, 액티비티 등)"
    )
    address: Optional[str] = Field(
        default=None,
        description="관광지 주소"
    )
    description: Optional[str] = Field(
        default=None,
        description="관광지 소개 텍스트"
    )
    spot_type: Optional[str] = Field(
        default=None,
        description="구분 (축제, 관광지, 체험, 카페 등)"
    )
    popularity_score: Optional[float] = Field(
        default=None,
        description="인기도 점수 (검색 결과/리뷰 수 기반)"
    )
    # source_urls: List[str] = Field(
    #     default_factory=list,
    #     description="데이터를 뽑아온 원본 URL들"
    # )
