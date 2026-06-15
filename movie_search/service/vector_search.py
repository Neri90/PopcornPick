from sentence_transformers import SentenceTransformer
from movie_search.repository.movie_repo import MovieRepository
from sqlalchemy.orm import Session

class VectorSearchService:
    _model = None

    def __init__(self, db: Session):
        self.repo = MovieRepository(db)
        if VectorSearchService._model is None:
            # SentenceTransformer 모델 로드 (384차원 출력을 내는 all-MiniLM-L6-v2)
            # 첫 실행 시 HuggingFace 허브에서 다운로드되며 이후 캐시됩니다.
            VectorSearchService._model = SentenceTransformer('all-MiniLM-L6-v2')

    def search(self, query_text: str, limit: int = 100):
        if not query_text.strip():
            return []
        
        # 검색어 임베딩 생성
        query_vector = VectorSearchService._model.encode(query_text).tolist()
        
        # DB에서 벡터 유사도 정렬 검색 수행
        return self.repo.search_vector(query_vector, limit=limit)
