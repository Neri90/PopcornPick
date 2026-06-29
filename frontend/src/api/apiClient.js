import axios from 'axios'

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
})

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config
        const isAuthRequest =
            originalRequest.url.includes('/auth/login') ||
            originalRequest.url.includes('/auth/refresh')

        if (error.response?.status === 401 && !isAuthRequest) {
            const refresh_token = localStorage.getItem('refresh_token')
            if (!refresh_token) return Promise.reject(error)
            const res = await apiClient.post('/auth/refresh', { refresh_token })
            localStorage.setItem('access_token', res.data.access_token)
            originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`
            return apiClient(originalRequest)
        }
        return Promise.reject(error)
    }
)

export default apiClient