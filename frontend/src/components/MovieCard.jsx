import styles from '../styles/MovieCard.module.css'

const MovieCard = ({ movie, rank, onClick }) => {
    return (
        <div className={styles.card} onClick={() => onClick(movie)}>
            {rank && <span className={styles.rank}>#{rank}</span>}
            <div className={styles.poster}>
                {movie.poster_path ? (
                    <img src={movie.poster_path} alt={movie.title} />
                ) : (
                    <div className={styles.noPoster}>No Image</div>
                )}
            </div>
            <div className={styles.info}>
                <p className={styles.titleKo}>{movie.title_ko || movie.title}</p>
                <p className={styles.title}>{movie.title}</p>
                <div className={styles.genres}>
                    {movie.genres.split('|').slice(0, 2).map((g) => (
                        <span key={g} className={styles.genreBadge}>{g}</span>
                    ))}
                </div>
                {movie.vote_average > 0 && (
                    <p className={styles.rating}>TMDB {movie.vote_average?.toFixed(1)}</p>
                )}
                {movie.score > 0 && (
                    <p className={styles.score}>선호도 {movie.score?.toFixed(2)}</p>
                )}
            </div>
        </div>
    )
}

export default MovieCard