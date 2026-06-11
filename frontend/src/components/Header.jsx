import { useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import styles from '../styles/Header.module.css'

const Header = () => {
    const { user, isLoggedIn, logout } = useAuthStore()
    const navigate = useNavigate()

    const handleLogout = () => {
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
                        <span className={styles.username}>{user?.username}</span>
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