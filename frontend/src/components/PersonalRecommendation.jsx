import useRecommendations from '../hooks/useRecommendations'
import MovieCard from './MovieCard'
import styles from '../styles/PersonalRecommendation.module.css'

const PersonalRecommendation = ({ userId, onMovieClick }) => {
    const { recommendations, loading, error, isFallback, refetch } = useRecommendations(userId)

    return (
        <section className={styles.section}>
            <div className={styles.header}>
                <div>
                    <h2 className={styles.title}>나만을 위한 추천</h2>
                    <p className={styles.desc}>
                        {isFallback
                            ? '아직 추천 데이터가 없어 인기 영화를 보여드립니다. 평점을 매기면 개인 맞춤으로 전환됩니다.'
                            : 'ALS 배치 알고리즘으로 계산된 개인화 추천 목록입니다.'}
                    </p>
                </div>
                <button className={styles.refreshBtn} onClick={refetch}>새로고침</button>
            </div>

            {loading && <p className={styles.status}>불러오는 중...</p>}
            {error && <p className={styles.error}>{error}</p>}

            {!loading && recommendations.length === 0 && !error && (
                <p className={styles.status}>표시할 추천 영화가 없습니다.</p>
            )}

            <div className={styles.cardList}>
                {recommendations.map((movie) => (
                    <MovieCard
                        key={movie.movie_id}
                        movie={movie}
                        rank={movie.rank}
                        onClick={onMovieClick}
                    />
                ))}
            </div>
        </section>
    )
}

export default PersonalRecommendation