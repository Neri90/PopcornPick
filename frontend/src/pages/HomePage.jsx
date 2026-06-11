import { useState } from 'react'
import useAuthStore from '../store/authStore'
import MovieSearchBar from '../components/MovieSearchBar'
import PersonalRecommendation from '../components/PersonalRecommendation'
import PopularMovies from '../components/PopularMovies'
import MovieDetailModal from '../components/MovieDetailModal'
import styles from '../styles/HomePage.module.css'

const HomePage = () => {
    const { user } = useAuthStore()
    const [selectedMovie, setSelectedMovie] = useState(null)

    const handleMovieClick = async (movie) => {
        setSelectedMovie(movie)
    }

    const handleCloseModal = () => {
        setSelectedMovie(null)
    }

    return (
        <div className={styles.page}>
            <MovieSearchBar onMovieClick={handleMovieClick} />

            <hr className={styles.divider} />

            <PersonalRecommendation
                userId={user?.user_id}
                onMovieClick={handleMovieClick}
            />

            <hr className={styles.divider} />

            <PopularMovies onMovieClick={handleMovieClick} />

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