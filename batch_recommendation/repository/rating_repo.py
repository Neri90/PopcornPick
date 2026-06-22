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


def fetch_user_rating(user_id: int, movie_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT rating FROM ratings
            WHERE user_id = %s AND movie_id = %s
        """, (user_id, movie_id))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
        conn.close()

def fetch_user_liked(user_id: int, movie_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 1 FROM user_click_logs
            WHERE user_id = %s AND movie_id = %s
            AND action_type = 'LIKE'
            LIMIT 1
        """, (user_id, movie_id))
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()