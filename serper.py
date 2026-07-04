import requests
from dotenv import load_dotenv
import os

load_dotenv()

serper_key = os.environ.get("SERPER_API_KEY")

url = "https://google.serper.dev/search"

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

headers = {
    "X-API-KEY": serper_key,
    "Content-Type": "application/json"
}

response = requests.request("POST" ,url, headers=headers, json=payload)

print(response.text)
