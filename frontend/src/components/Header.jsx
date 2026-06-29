import { useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import styles from '../styles/Header.module.css'
import apiClient from '../api/apiClient'

const Header = () => {
    const { user, isLoggedIn, logout } = useAuthStore()
    const navigate = useNavigate()

    const handleLogout = async () => {
        const refresh_token = localStorage.getItem('refresh_token')
        await apiClient.post('/auth/logout', { refresh_token })
        logout()
        navigate('/login')
    }

    return (
        <header className={styles.header}>
            <div className={styles.logo} onClick={() => navigate('/')}>
                PopcornPick
            </div>
            <div className={styles.right}>
                {isLoggedIn ? (
                    <>
                        <span
                            className={styles.username}
                            onClick={() => navigate('/profile')}
                            style={{ cursor: 'pointer' }}
                        >
                            {user?.username}
                        </span>
                        <button className={styles.logoutBtn} onClick={handleLogout}>로그아웃</button>
                    </>
                ) : (
                    <button className={styles.loginBtn} onClick={() => navigate('/login')}>로그인</button>
                )}
            </div>
        </header>
    )
}

export default Header