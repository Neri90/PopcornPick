import { useState } from 'react'
import useMovieSearch from '../hooks/useMovieSearch'
import MovieCard from './MovieCard'
import styles from '../styles/MovieSearchBar.module.css'

const MovieSearchBar = ({ onMovieClick }) => {
    const [input, setInput] = useState('')
    const { results, loading, error, search, clearResults } = useMovieSearch()

    const handleSearch = (e) => {
        e.preventDefault()
        if (input.trim()) search(input)
    }

    const handleClear = () => {
        setInput('')
        clearResults()
    }

    return (
        <section className={styles.section}>
            <h2 className={styles.title}>영화 검색</h2>
            <p className={styles.desc}>키워드 검색과 의미론적 벡터 검색을 결합해 최적의 영화를 찾아드립니다.</p>

            <form className={styles.form} onSubmit={handleSearch}>
                <input
                    className={styles.input}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="영화 제목 또는 분위기를 입력하세요. 예: 슬픈 로맨스, 우주 어드벤처"
                />
                <button className={styles.searchBtn} type="submit">검색</button>
                {results.length > 0 && (
                    <button className={styles.clearBtn} type="button" onClick={handleClear}>초기화</button>
                )}
            </form>

            {loading && <p className={styles.status}>검색 중...</p>}
            {error && <p className={styles.error}>{error}</p>}

            {results.length > 0 && (
                <div className={styles.results}>
                    <p className={styles.resultCount}>검색 결과 {results.length}개</p>
                    <div className={styles.cardList}>
                        {results.map((movie, idx) => (
                            <MovieCard
                                key={movie.movie_id}
                                movie={movie}
                                onClick={onMovieClick}
                            />
                        ))}
                    </div>
                </div>
            )}
        </section>
    )
}

export default MovieSearchBar