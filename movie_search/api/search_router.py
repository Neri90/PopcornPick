from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from movie_search.service.fulltext_search import FullTextSearchService
from movie_search.service.vector_search import VectorSearchService
from movie_search.service.hybrid_merger import HybridSearchService
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MovieSearchResult(BaseModel):
    movie_id: int
    ml_movie_id: int
    title: str
    title_ko: Optional[str] = None
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    vote_average: float
    release_year: Optional[int] = None
    tmdb_id: Optional[int] = None
    genres: str
    click_count: int
    avg_rating: float
    score: float

class SearchResponse(BaseModel):
    query: str
    type: str
    results: List[MovieSearchResult]

@router.get("", response_model=SearchResponse)
def search_movies(
    q: str = Query(..., description="검색 키워드"),
    limit: int = Query(10, ge=1, le=100, description="반환할 영화 개수"),
    type: str = Query("hybrid", description="검색 타입 (hybrid, vector, fulltext)"),
    db: Session = Depends(get_db)
):
    """
    영화 하이브리드 검색 API 엔드포인트입니다.
    - **hybrid**: Vector Search와 Full-Text Search를 RRF 알고리즘으로 결합하여 정밀한 결과를 리턴합니다.
    - **vector**: 쿼리 텍스트를 임베딩(all-MiniLM-L6-v2)하여 pgvector 코사인 유사도로 정렬 검색합니다.
    - **fulltext**: PostgreSQL Full-Text Search(형태소/텍스트 인덱싱) 기반 검색 결과를 리턴합니다.
    """
    search_type = type.lower()
    if search_type not in ["hybrid", "vector", "fulltext"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 검색 타입입니다. (hybrid, vector, fulltext 중 선택)")

    if search_type == "vector":
        service = VectorSearchService(db)
        results = service.search(q, limit=limit)
    elif search_type == "fulltext":
        service = FullTextSearchService(db)
        results = service.search(q, limit=limit)
    else:  # hybrid
        service = HybridSearchService(db)
        results = service.search(q, limit=limit)

    return {
        "query": q,
        "type": search_type,
        "results": results
    }
