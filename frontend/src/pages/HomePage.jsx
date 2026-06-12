import {useState} from 'react'
import MovieSearchBar from '../components/MovieSearchBar'
import PersonalRecommendation from '../components/PersonalRecommendation'
import PopularMovies from '../components/PopularMovies'
import MovieDetailModal from '../components/MovieDetailModal'
import styles from '../styles/HomePage.module.css'
import apiClient from '../api/apiClient'

const HomePage = () => {
    const [selectedMovie, setSelectedMovie] = useState(null)

    // HomePage.jsx
    const handleMovieClick = async (movie) => {
        // 클릭 로그 전송
        try {
            await apiClient.post('/logs', {
                user_id: 1,  // 임시
                movie_id: movie.movie_id,
                genres: movie.genres,
                action_type: 'CLICK'
            })
        } catch (err) {
            console.error('클릭 로그 실패:', err)
        }
        setSelectedMovie(movie)
    }

    const handleCloseModal = () => {
        setSelectedMovie(null)
    }

    return (
        <div className={styles.page}>
            <MovieSearchBar onMovieClick={handleMovieClick}/>

            <hr className={styles.divider}/>

            <PersonalRecommendation
                userId={1}
                onMovieClick={handleMovieClick}
            />

            <hr className={styles.divider}/>

            <PopularMovies onMovieClick={handleMovieClick}/>

            {selectedMovie && (
                <MovieDetailModal
                    movie={selectedMovie}
                    onClose={handleCloseModal}
                />
            )}
        </div>
    )
}

export default HomePage