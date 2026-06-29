import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import apiClient from '../api/apiClient'
import useAuthStore from '../store/authStore'
import styles from '../styles/LoginPage.module.css'

const LoginPage = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const { login } = useAuthStore()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            const res = await apiClient.post('/auth/login', { email, password })
            const { access_token, user_id, username, refresh_token } = res.data
            login({ user_id, username, email }, access_token, refresh_token)
            localStorage.setItem('user', JSON.stringify({ user_id, username, email }))
            navigate('/')
        } catch (err) {
            const detail = err.response?.data?.detail
            setError(Array.isArray(detail) ? detail[0]?.msg : (typeof detail === 'string' ? detail : '로그인에 실패했습니다.'))
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <h1 className={styles.logo}>PopcornPick</h1>
                <p className={styles.subtitle}>개인화 영화 추천 플랫폼</p>

                <form className={styles.form} onSubmit={handleSubmit}>
                    <div className={styles.field}>
                        <label>이메일</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="이메일 입력"
                            required
                        />
                    </div>
                    <div className={styles.field}>
                        <label>비밀번호</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="비밀번호 입력"
                            required
                        />
                    </div>
                    {error && <p className={styles.error}>{error}</p>}
                    <button className={styles.btn} type="submit" disabled={loading}>
                        {loading ? '로그인 중...' : '로그인'}
                    </button>
                </form>

                <p className={styles.link}>
                    계정이 없으신가요? <Link to="/register">회원가입</Link>
                </p>
            </div>
        </div>
    )
}

export default LoginPage