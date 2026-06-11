import { create } from 'zustand'

const useAuthStore = create((set) => ({
    user: null,
    isLoggedIn: false,

    login: (userData, token) => {
        localStorage.setItem('access_token', token)
        set({ user: userData, isLoggedIn: true })
    },

    logout: () => {
        localStorage.removeItem('access_token')
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