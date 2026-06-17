def upsert_rating(conn, payload):
    with conn.cursor() as cursor:
        sql = """
            INSERT INTO ratings
            (
                user_id,
                movie_id,
                rating
            )
            VALUES (%s,%s,%s)
            
            ON CONFLICT(user_id, movie_id)
            DO UPDATE SET
                rating = EXCLUDED.rating,
                rated_at = now()
        """

        cursor.execute(
            sql,
            (
                payload.user_id,
                payload.movie_id,
                payload.rating_value
            )
        )



def insert_log(conn, payload):
    with conn.cursor() as cursor:
        sql = """
        INSERT INTO user_click_logs
        (
            user_id,
            movie_id,
            genres,
            action_type,
            rating_value
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                payload.user_id,
                payload.movie_id,
                payload.genres,
                payload.action_type,
                payload.rating_value
            )
        )