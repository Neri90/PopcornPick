from realtime_log.repository.log_repo import insert_log, upsert_rating
from db import get_connection

def save_log(payload):
    print("입력정보 : ",payload)

    conn = get_connection()

    try:
        action_type = payload.action_type.upper()

        if action_type not in ["CLICK", "LIKE", "RATING"]:
            raise ValueError("invalid action_type")

        if action_type == "RATING":
            upsert_rating(conn, payload)
        
        insert_log(conn, payload)

        conn.commit()

    except Exception as e:
        print(f"[ACTION_ERROR] {e}")
        conn.rollback()
        raise
    finally:
        conn.close()