import usePopularMovies from '../hooks/usePopularMovies'
import MovieCard from './MovieCard'
import styles from '../styles/PopularMovies.module.css'

const PopularMovies = ({ onMovieClick }) => {
    const { movies, loading, error } = usePopularMovies(10)

    return (
        <section className={styles.section}>
            <h2 className={styles.title}>인기 영화</h2>
            <p className={styles.desc}>유저들이 가장 많이 클릭하고 평점을 준 영화들입니다.</p>

            {loading && <p className={styles.status}>불러오는 중...</p>}
            {error && <p className={styles.error}>{error}</p>}

            <div className={styles.cardList}>
                {movies.map((movie, idx) => (
                    <MovieCard
                        key={movie.movie_id}
                        movie={movie}
                        rank={idx + 1}
                        onClick={onMovieClick}
                    />
                ))}
            </div>
        </section>
    )
}

export default PopularMovies