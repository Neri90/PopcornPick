import { useState } from 'react'
import apiClient from '../api/apiClient'
import useAuthStore from '../store/authStore'
import styles from '../styles/MovieDetailModal.module.css'

const MovieDetailModal = ({ movie, onClose }) => {
    const { user } = useAuthStore()
    const [rating, setRating] = useState(0)
    const [liked, setLiked] = useState(false)
    const [message, setMessage] = useState('')

    if (!movie) return null

    const sendLog = async (action_type, rating_value = null) => {
        try {
            const endpoint = action_type === 'LIKE' ? '/logs/like'
                           : action_type === 'RATING' ? '/logs/rating'
                           : '/logs/click'
            await apiClient.post(endpoint, {
                user_id: user.user_id,
                movie_id: movie.movie_id,
                genres: movie.genres,
                rating_value,
            })
        } catch (err) {
            console.error('로그 전송 실패:', err)
        }
    }

    const handleLike = async () => {
        await sendLog('LIKE')
        setLiked(true)
        setMessage('찜 목록에 추가됐어요!')
    }

    const handleRating = async (value) => {
        setRating(value)
        await sendLog('RATING', value)
        setMessage(`${value}점 평점이 등록됐어요!`)
    }

    return (
        <div className={styles.overlay} onClick={onClose}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <button className={styles.closeBtn} onClick={onClose}>×</button>

                <div className={styles.content}>
                    <div className={styles.left}>
                        {movie.poster_path ? (
                            <img src={movie.poster_path} alt={movie.title} className={styles.poster} />
                        ) : (
                            <div className={styles.noPoster}>No Image</div>
                        )}
                    </div>

                    <div className={styles.right}>
                        <h2 className={styles.titleKo}>{movie.title_ko || movie.title}</h2>
                        <p className={styles.title}>{movie.title}</p>

                        <div className={styles.genres}>
                            {movie.genres.split('|').map((g) => (
                                <span key={g} className={styles.genreBadge}>{g}</span>
                            ))}
                        </div>

                        {movie.vote_average > 0 && (
                            <p className={styles.voteAverage}>TMDB 평점: {movie.vote_average?.toFixed(1)}</p>
                        )}

                        <div className={styles.ratingSection}>
                            <p className={styles.ratingLabel}>내 평점</p>
                            <div className={styles.stars}>
                                {[1, 2, 3, 4, 5].map((star) => (
                                    <button
                                        key={star}
                                        className={`${styles.star} ${rating >= star ? styles.active : ''}`}
                                        onClick={() => handleRating(star)}
                                    >
                                        ★
                                    </button>
                                ))}
                            </div>
                        </div>

                        {message && <p className={styles.message}>{message}</p>}

                        <div className={styles.actions}>
                            <button
                                className={`${styles.likeBtn} ${liked ? styles.liked : ''}`}
                                onClick={handleLike}
                                disabled={liked}
                            >
                                {liked ? '찜 완료 ❤️' : '찜하기'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MovieDetailModal