import { useState } from 'react'
import apiClient from '../api/apiClient'

const useMovieSearch = () => {
    const [results, setResults] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [query, setQuery] = useState('')

    const search = async (q) => {
        if (!q.trim()) {
            setResults([])
            return
        }
        setQuery(q)
        setLoading(true)
        setError(null)
        try {
            const res = await apiClient.get('/search', { params: { q, limit: 10 } })
            setResults(res.data.results || [])
        } catch (err) {
            setError('검색 중 오류가 발생했습니다.')
        } finally {
            setLoading(false)
        }
    }

    const clearResults = () => {
        setResults([])
        setQuery('')
    }

    return { results, loading, error, query, search, clearResults }
}

export default useMovieSearch