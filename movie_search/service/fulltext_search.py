from movie_search.repository.movie_repo import MovieRepository
from sqlalchemy.orm import Session

class FullTextSearchService:
    def __init__(self, db: Session):
        self.repo = MovieRepository(db)

    def search(self, query_text: str, limit: int = 100):
        if not query_text.strip():
            return []
        
        # PostgreSQL Full-Text Search 질의 실행
        return self.repo.search_fulltext(query_text, limit=limit)
