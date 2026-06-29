import { create } from 'zustand'

const savedToken = localStorage.getItem('access_token')
const savedUser = JSON.parse(localStorage.getItem('user') || 'null')

const useAuthStore = create((set) => ({
    user: savedToken && savedUser ? savedUser : null,
    isLoggedIn: !!(savedToken && savedUser),

    login: (userData, token, refresh_token) => {
        localStorage.setItem('access_token', token)
        localStorage.setItem('refresh_token', refresh_token)
        set({ user: userData, isLoggedIn: true })
    },

    logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null, isLoggedIn: false })
    },

    initAuth: () => {
        const token = localStorage.getItem('access_token')
        if (!token) return
        // 토큰 있으면 로컬스토리지에서 유저 정보 복원
        const user = JSON.parse(localStorage.getItem('user') || 'null')
        if (user) set({ user, isLoggedIn: true })
    },
}))

export default useAuthStore