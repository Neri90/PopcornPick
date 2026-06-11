import { useState, useEffect } from 'react'
import apiClient from '../api/apiClient'

const useRecommendations = (userId) => {
    const [recommendations, setRecommendations] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [isFallback, setIsFallback] = useState(false)

    const fetchRecommendations = async () => {
        if (!userId) return
        setLoading(true)
        setError(null)
        try {
            const res = await apiClient.get(`/recommendations/${userId}`)
            setRecommendations(res.data.recommendations)
            setIsFallback(false)
        } catch (err) {
            if (err.response?.status === 404) {
                setIsFallback(true)
                setRecommendations([])
            } else {
                setError('추천 데이터를 불러오지 못했습니다.')
            }
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchRecommendations()
    }, [userId])

    return { recommendations, loading, error, isFallback, refetch: fetchRecommendations }
}

export default useRecommendations