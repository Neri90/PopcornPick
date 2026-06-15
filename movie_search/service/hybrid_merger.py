from movie_search.service.fulltext_search import FullTextSearchService
from movie_search.service.vector_search import VectorSearchService
from sqlalchemy.orm import Session

class HybridSearchService:
    def __init__(self, db: Session):
        self.fts_service = FullTextSearchService(db)
        self.vs_service = VectorSearchService(db)

    def search(self, query_text: str, limit: int = 10, k: int = 60, fetch_limit: int = 100):
        """
        Full-Text Search 결과와 Vector Search 결과를 가져와서 RRF (Reciprocal Rank Fusion) 알고리즘으로 병합합니다.
        """
        if not query_text.strip():
            return []

        # RRF 점수의 정밀도를 높이기 위해, 각각의 검색 엔진에서 최종 반환 수보다 넉넉히(fetch_limit) 가져옵니다.
        fts_results = self.fts_service.search(query_text, limit=fetch_limit)
        vs_results = self.vs_service.search(query_text, limit=fetch_limit)

        rrf_scores = {}
        lookup = {}

        # Vector Search 결과에 대한 가중치 계산 (1-based rank)
        for rank, movie in enumerate(vs_results, start=1):
            mid = movie['movie_id']
            rrf_scores[mid] = rrf_scores.get(mid, 0.0) + 1.0 / (k + rank)
            lookup[mid] = movie

        # Full-Text Search 결과에 대한 가중치 계산 (1-based rank)
        for rank, movie in enumerate(fts_results, start=1):
            mid = movie['movie_id']
            rrf_scores[mid] = rrf_scores.get(mid, 0.0) + 1.0 / (k + rank)
            # FTS 결과가 벡터 검색 결과보다 더 상세한 정보를 담고 있을 경우를 고려하여 정보 업데이트
            lookup[mid] = movie

        # RRF 점수 내림차순 정렬
        sorted_movies = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        merged_results = []
        for mid, score in sorted_movies[:limit]:
            movie_data = lookup[mid].copy()
            movie_data['score'] = score
            movie_data['rrf_score'] = score
            merged_results.append(movie_data)

        return merged_results
