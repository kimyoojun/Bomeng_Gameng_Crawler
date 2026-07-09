import os
from dotenv import load_dotenv
from openai import OpenAI

from schemas.travel_destination import TouristSpotExtract

load_dotenv()

openai = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

# system prompt 작성
SYSTEM_PROMPT = """
너는 한국 여행지 메타데이터 추출기다.
입력된 본문 텍스트를 읽고 TouristSpotExtract 스키마에 맞는 값만 추출하라.

중요 규칙:
1. companions는 반드시 다음 값만 사용:
   - family
   - couple
   - friends
   - solo
   - parents

2. 원문 표현을 표준값으로 정규화:
   - 연인, 커플, 여자친구, 남자친구, 애인, 데이트 -> couple
   - 가족, 아이와, 아이랑, 아기와, 유아 동반 -> family
   - 부모님, 어머니, 아버지, 엄마, 아빠 모시고 -> parents
   - 친구, 친구들, 동기, 지인들과 -> friends
   - 혼자, 솔로, 나홀로, 1인 여행 -> solo

3. categories는 반드시 다음 값만 사용:
   - healing
   - nature
   - activity
   - culture
   - food
   - photo

4. 카테고리 정규화 예시:
   - 힐링, 여유, 조용함, 휴식 -> healing
   - 자연, 바다, 숲, 산, 풍경 -> nature
   - 체험, 물놀이, 액티비티, 레저 -> activity
   - 전시, 역사, 박물관, 문화 -> culture
   - 맛집, 먹거리, 음식 -> food
   - 사진, 포토존, 인생샷 -> photo

5. 원문에 근거가 없는 값은 넣지 말 것.
6. 본문에 없는 내용은 절대 추측하지 말 것
7. 본문에서 근거를 찾을 수 없는 필드는 빈값으로 둘 것
8. 문자열 필드에 정보가 없으면 null 반환
9. 리스트 필드에 정보가 없으면 빈 리스트 [] 반환
10. JSON 외 다른 문장은 출력하지 말 것.
"""

# 관광지를 TouristSpotExtract에 맞게 추출하는 함수
def extract_tourist_spot(text: str):
    
    completion = openai.beta.chat.completions.parse(
    model = "gpt-4o-mini",
    messages = [
        {
            "role": "system", 
            "content": SYSTEM_PROMPT
         },
        {
            "role": "user",
            "content": f"다음 관광지 본문에서 정보를 추출해줘: \n\n{text}"
        },
    ],

    response_format = TouristSpotExtract,
    )

    return completion.choices[0].message.parsed
