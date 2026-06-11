import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import apiClient from '../api/apiClient'
import styles from '../styles/RegisterPage.module.css'

const RegisterPage = () => {
    const [form, setForm] = useState({ username: '', email: '', password: '' })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            await apiClient.post('/auth/register', form)
            navigate('/login')
        } catch (err) {
            setError(err.response?.data?.detail || '회원가입에 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <h1 className={styles.logo}>PopcornPick</h1>
                <p className={styles.subtitle}>회원가입</p>

                <form className={styles.form} onSubmit={handleSubmit}>
                    <div className={styles.field}>
                        <label>닉네임</label>
                        <input
                            type="text"
                            name="username"
                            value={form.username}
                            onChange={handleChange}
                            placeholder="닉네임 입력"
                            required
                        />
                    </div>
                    <div className={styles.field}>
                        <label>이메일</label>
                        <input
                            type="email"
                            name="email"
                            value={form.email}
                            onChange={handleChange}
                            placeholder="이메일 입력"
                            required
                        />
                    </div>
                    <div className={styles.field}>
                        <label>비밀번호</label>
                        <input
                            type="password"
                            name="password"
                            value={form.password}
                            onChange={handleChange}
                            placeholder="비밀번호 입력"
                            required
                        />
                    </div>
                    {error && <p className={styles.error}>{error}</p>}
                    <button className={styles.btn} type="submit" disabled={loading}>
                        {loading ? '처리 중...' : '회원가입'}
                    </button>
                </form>

                <p className={styles.link}>
                    이미 계정이 있으신가요? <Link to="/login">로그인</Link>
                </p>
            </div>
        </div>
    )
}

export default RegisterPage