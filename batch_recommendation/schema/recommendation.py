from pydantic import BaseModel
from typing import Optional

class RecommendationItem(BaseModel):
    movie_id: int
    title: str
    title_ko: Optional[str] = None
    genres: str
    poster_path: Optional[str] = None
    vote_average: Optional[float] = None
    score: float
    rank: int

class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: list[RecommendationItem]