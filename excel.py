# 데이터를 엑셀로 저장

import pandas as pd

# 데이터를 엑셀로 저장하는 함수
def data_excel(data: list):
    df = pd.DataFrame(data, columns = ["name", "spot_type", "address", "description", "categories", "companions"])
    df.to_excel("jeju_spot.xlsx")
