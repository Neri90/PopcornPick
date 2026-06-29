import { useState, useEffect } from 'react'
import apiClient from '../api/apiClient'
import styles from '../styles/ProfilePage.module.css'

const ProfilePage = () => {
    const [profile, setProfile] = useState(null)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [message, setMessage] = useState('')

    useEffect(() => {
        apiClient.get('/auth/me')
            .then((res) => setProfile(res.data))
    }, [])

    const handleUpdate = async (e) => {
        e.preventDefault()
        const res = await apiClient.put('/auth/profile', { username, password })
        setProfile(res.data)
        setMessage('수정이 완료되었습니다.')
        setUsername('')
        setPassword('')
    }

    if (!profile) return <p className={styles.loading}>로딩 중...</p>

    const joinedDate = new Date(profile.created_at).toLocaleDateString('ko-KR')

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <h1 className={styles.title}>내 정보</h1>

                <div className={styles.infoList}>
                    <div className={styles.infoRow}>
                        <span className={styles.infoLabel}>이름</span>
                        <span className={styles.infoValue}>{profile.username}</span>
                    </div>
                    <div className={styles.infoRow}>
                        <span className={styles.infoLabel}>이메일</span>
                        <span className={styles.infoValue}>{profile.email}</span>
                    </div>
                    <div className={styles.infoRow}>
                        <span className={styles.infoLabel}>가입일</span>
                        <span className={styles.infoValue}>{joinedDate}</span>
                    </div>
                </div>

                <h2 className={styles.sectionTitle}>회원정보 수정</h2>
                <form className={styles.form} onSubmit={handleUpdate}>
                    <div className={styles.field}>
                        <label>새 닉네임</label>
                        <input
                            type="text"
                            placeholder="새 닉네임"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div className={styles.field}>
                        <label>새 비밀번호</label>
                        <input
                            type="password"
                            placeholder="새 비밀번호"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button className={styles.btn} type="submit">수정하기</button>
                    {message && <p className={styles.message}>{message}</p>}
                </form>
            </div>
        </div>
    )
}

export default ProfilePage