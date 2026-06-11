from psycopg2.extras import execute_values
from db import get_connection


def save_recommendations(rows: list):
    if not rows:
        print("저장할 추천 데이터 없음")
        return

    conn = get_connection()
    try:
        cur = conn.cursor()

        batch_run_at = rows[0][4]
        user_ids = list(set(r[0] for r in rows))

        execute_values(cur, """
            INSERT INTO recommendations (user_id, movie_id, score, rank, batch_run_at)
            VALUES %s
        """, rows)

        cur.execute("""
            DELETE FROM recommendations
            WHERE user_id = ANY(%s)
            AND batch_run_at < %s
        """, (user_ids, batch_run_at))

        cur.execute("""
            UPDATE movies
            SET avg_rating = sub.avg
            FROM (
                SELECT movie_id, AVG(rating) AS avg
                FROM ratings
                GROUP BY movie_id
            ) sub
            WHERE movies.movie_id = sub.movie_id
        """)

        conn.commit()
        print(f"recommendations 저장 완료: {len(rows)}건")

    except Exception as e:
        conn.rollback()
        print(f"Error saving recommendations: {e}")
    finally:
        cur.close()
        conn.close()


def fetch_recommendations(user_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT r.movie_id, m.title, m.title_ko, m.genres,
                   m.poster_path, m.vote_average, r.score, r.rank
            FROM recommendations r
            JOIN movies m ON r.movie_id = m.movie_id
            WHERE r.user_id = %s
            AND r.batch_run_at = (
                SELECT MAX(batch_run_at)
                FROM recommendations
                WHERE user_id = %s
            )
            ORDER BY r.rank
        """, (user_id, user_id))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def fetch_popular_fallback(limit=20):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT movie_id, title, title_ko, genres,
                   poster_path, vote_average, avg_rating
            FROM movies
            ORDER BY avg_rating DESC, click_count DESC
            LIMIT %s
        """, (limit,))
        return [
            {
                "movie_id":     row[0],
                "title":        row[1],
                "title_ko":     row[2],
                "genres":       row[3],
                "poster_path":  row[4],
                "vote_average": row[5],
                "score":        row[6],
                "rank":         idx + 1
            }
            for idx, row in enumerate(cur.fetchall())
        ]
    except Exception as e:
        print(f"Error fetching fallback: {e}")
        return []
    finally:
        cur.close()
        conn.close()