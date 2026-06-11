from db import get_connection

def fetch_als_input():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
                    SELECT DISTINCT
                    ON (user_id, movie_id)
                        user_id, movie_id, rating
                    FROM (
                        SELECT user_id, movie_id, rating, rated_at AS ts
                        FROM ratings
                        UNION ALL
                        SELECT user_id, movie_id, rating_value, logged_at AS ts
                        FROM user_click_logs
                        WHERE action_type = 'RATING'
                        AND rating_value IS NOT NULL
                        ) combined
                    ORDER BY user_id, movie_id, ts DESC
                    """)
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching als input: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def upsert_rating(user_id: int, movie_id: int, rating: float):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ratings (user_id, movie_id, rating)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, movie_id)
            DO UPDATE SET rating = EXCLUDED.rating, rated_at = NOW()
        """, (user_id, movie_id, rating))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error upserting rating: {e}")
    finally:
        cur.close()
        conn.close()