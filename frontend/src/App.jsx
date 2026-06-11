import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import useAuthStore from './store/authStore'
import Header from './components/Header'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import HomePage from './pages/HomePage'
import styles from './styles/App.module.css'

const PrivateRoute = ({ children }) => {
    const { isLoggedIn } = useAuthStore()
    return isLoggedIn ? children : <Navigate to="/login" />
}

const App = () => {
    const { initAuth } = useAuthStore()

    useEffect(() => {
        initAuth()
    }, [])

    return (
        <BrowserRouter>
            <div className={styles.app}>
                <Header />
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/" element={
                        <PrivateRoute>
                            <HomePage />
                        </PrivateRoute>
                    } />
                </Routes>
            </div>
        </BrowserRouter>
    )
}

export default App