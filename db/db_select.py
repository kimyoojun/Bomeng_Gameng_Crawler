from db.supabase_client import supabase

# db에서 관광지명을 가져오는 함수
def select_spot():
    select = (
        supabase
        .table("jeju_tourist")
        .select("관광지명")
        .execute()
    ) 

    return select.data
    