import pandas as pd
import psycopg2
import os
from psycopg2.extras import execute_values

def get_conn():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        dbname=os.getenv('POSTGRES_DB', 'popcornpick'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
    )

def load_movies(conn):
    print("movies_processed.csv 로드 중...")
    df = pd.read_csv('data/raw/movies_processed.csv', encoding='utf-8-sig')
    print(f"영화 수: {len(df)}개")

    cur = conn.cursor()
    rows = [
        (
            int(row['ml_movie_id']),
            str(row['title']),
            str(row['title_ko'])      if pd.notna(row['title_ko'])      else None,
            str(row['overview'])      if pd.notna(row['overview'])       else None,
            str(row['poster_path'])   if pd.notna(row['poster_path'])    else None,
            float(row['vote_average']) if pd.notna(row['vote_average'])  else 0.0,
            int(row['release_year'])  if pd.notna(row['release_year'])   else None,
            int(row['tmdb_id'])       if pd.notna(row['tmdb_id'])        else None,
            str(row['genres'])        if pd.notna(row['genres'])         else '',
            str(row['search_text'])   if pd.notna(row['search_text'])    else '',
            str(row['embedding']),
        )
        for _, row in df.iterrows()
    ]

    execute_values(cur, """
        INSERT INTO movies (
            ml_movie_id, title, title_ko, overview, poster_path,
            vote_average, release_year, tmdb_id, genres, search_text, embedding
        )
        VALUES %s
        ON CONFLICT (ml_movie_id) DO NOTHING
    """, rows)

    conn.commit()
    print(f"movies 적재 완료: {len(rows)}개")
    cur.close()

def load_users(conn):
    print("\nratings.csv 로드 중...")
    ratings_df = pd.read_csv('data/raw/ratings.csv')
    user_ids = sorted(ratings_df['userId'].unique())
    print(f"고유 유저 수: {len(user_ids)}개")

    cur = conn.cursor()
    rows = [
        (
            f"ml_user_{uid}",
            f"ml_user_{uid}@movielens.org",
            "movielens_dummy_password",
        )
        for uid in user_ids
    ]

    execute_values(cur, """
        INSERT INTO users (username, email, password)
        VALUES %s
        ON CONFLICT (email) DO NOTHING
    """, rows)

    conn.commit()
    print(f"users 적재 완료: {len(rows)}개")
    cur.close()

def load_ratings(conn):
    print("\nratings 적재 중...")
    ratings_df = pd.read_csv('data/raw/ratings.csv')

    cur = conn.cursor()

    cur.execute("SELECT user_id, username FROM users WHERE username LIKE 'ml_user_%'")
    user_map = {int(row[1].replace('ml_user_', '')): row[0] for row in cur.fetchall()}

    cur.execute("SELECT movie_id, ml_movie_id FROM movies")
    movie_map = {row[1]: row[0] for row in cur.fetchall()}

    rows = []
    skip = 0
    for _, row in ratings_df.iterrows():
        uid = int(row['userId'])
        mid = int(row['movieId'])
        if uid not in user_map or mid not in movie_map:
            skip += 1
            continue
        rows.append((user_map[uid], movie_map[mid], float(row['rating'])))

    batch_size = 10000
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        execute_values(cur, """
            INSERT INTO ratings (user_id, movie_id, rating)
            VALUES %s
            ON CONFLICT (user_id, movie_id) DO NOTHING
        """, batch)
        print(f"진행: {min(i + batch_size, len(rows))}/{len(rows)}")

    conn.commit()
    print(f"ratings 적재 완료: {len(rows)}개 (스킵: {skip}개)")
    cur.close()

def update_avg_rating(conn):
    print("\navg_rating 갱신 중...")
    cur = conn.cursor()
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
    print("avg_rating 갱신 완료")
    cur.close()

if __name__ == "__main__":
    conn = get_conn()
    try:
        load_movies(conn)
        load_users(conn)
        load_ratings(conn)
        update_avg_rating(conn)
        print("\n전체 완료")
    except Exception as e:
        conn.rollback()
        print(f"오류 발생: {e}")
        raise
    finally:
        conn.close()