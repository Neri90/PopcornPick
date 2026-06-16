from db import get_connection
from typing import Optional, Tuple

def create_user(username: str, email: str, password: str) -> Optional[Tuple]:
    """
    새로운 유저를 DB의 users 테이블에 INSERT하고 생성된 레코드를 튜플 형태로 반환합니다.
    """
    # TODO: 데이터베이스 연결(get_connection)을 사용하여 안전한 INSERT 쿼리를 실행하세요.
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""insert into users (username, email, password) 
                    values (%s, %s, %s) 
                    returning user_id, email, username, created_at""",
                    (username, email, password))
        conn.commit()
        return cur.fetchone()
    except Exception as e:
        conn.rollback()
        print(f'회원가입 실패: {e}')
        return None
    finally:
        cur.close()
        conn.close()

def get_user_by_email(email: str) -> Optional[Tuple]:
    """
    이메일을 기반으로 사용자를 조회하여 튜플 형태로 반환합니다.
    """
    # TODO: 데이터베이스 연결(get_connection)을 사용하여 SELECT 쿼리를 실행하세요.
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('select user_id, username, email, password, created_at from users where email = %s', (email,))
        return cur.fetchone()
    except Exception as e:
        print('이메일 조회 불가')
        return None
    finally:
        cur.close()
        conn.close()

def get_user_by_id(user_id: int) -> Optional[Tuple]:
    """
    유저 ID를 기반으로 사용자를 조회하여 튜플 형태로 반환합니다.
    """
    # TODO: 데이터베이스 연결(get_connection)을 사용하여 SELECT 쿼리를 실행하세요.
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('select user_id, username, email, password, created_at from users where user_id = %s',(user_id,))
        return cur.fetchone()
    except Exception as e:
        print('이메일 조회 불가')
        return None
    finally:
        cur.close()
        conn.close()
