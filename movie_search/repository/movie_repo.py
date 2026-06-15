from sqlalchemy.orm import Session
from sqlalchemy import text

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_fulltext(self, query_text: str, limit: int = 100):
        """
        PostgreSQL Full-Text Search를 사용하여 영화를 검색합니다.
        GIN 인덱스(idx_movies_fulltext)를 활용하며, ts_rank_cd로 유사도 정렬합니다.
        """
        sql = text("""
            SELECT movie_id, ml_movie_id, title, title_ko, overview, poster_path, vote_average, 
                   release_year, tmdb_id, genres, click_count, avg_rating,
                   ts_rank_cd(to_tsvector('simple', coalesce(search_text, '')), plainto_tsquery('simple', :query)) AS score
            FROM movies
            WHERE to_tsvector('simple', coalesce(search_text, '')) @@ plainto_tsquery('simple', :query)
            ORDER BY score DESC
            LIMIT :limit
        """)
        result = self.db.execute(sql, {"query": query_text, "limit": limit})
        return [dict(row._mapping) for row in result]

    def search_vector(self, query_vector: list, limit: int = 100):
        """
        pgvector의 cosine distance(<=>)를 사용하여 벡터 유사도 기반 영화를 검색합니다.
        """
        vector_str = "[" + ",".join(map(str, query_vector)) + "]"
        sql = text("""
            SELECT movie_id, ml_movie_id, title, title_ko, overview, poster_path, vote_average, 
                   release_year, tmdb_id, genres, click_count, avg_rating,
                   (1.0 - (embedding <=> CAST(:vector AS vector))) AS score
            FROM movies
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:vector AS vector) ASC
            LIMIT :limit
        """)
        result = self.db.execute(sql, {"vector": vector_str, "limit": limit})
        return [dict(row._mapping) for row in result]
