import { useState, useEffect } from 'react'
import apiClient from '../api/apiClient'

const usePopularMovies = (limit = 10) => {
    const [movies, setMovies] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchPopular = async () => {
            setLoading(true)
            setError(null)
            try {
                const res = await apiClient.get('/movies/popular', { params: { limit } })
                setMovies(res.data)
            } catch (err) {
                setError('인기 영화를 불러오지 못했습니다.')
            } finally {
                setLoading(false)
            }
        }
        fetchPopular()
    }, [limit])

    return { movies, loading, error }
}

export default usePopularMovies