from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Tuple

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password: str) -> Optional[Tuple]:
        """
        새로운 유저를 DB의 users 테이블에 INSERT하고 생성된 레코드를 튜플 형태로 반환합니다.
        """
        sql = text("""
                    insert into users (username, email, password)
                    values (:username, :email, :password)
                    returning user_id, email, username, created_at
                   """)
        result = self.db.execute(sql,{"username":username,"email":email,"password":password})
        self.db.commit()
        row = result.fetchone()
        return dict(row._mapping) if row else None

    def update_user(self, user_id: int, username: str | None, password: str | None) -> Optional[Tuple]:
        """
        회원이 username, password를 선택적으로 수정할 수 있도록 함
        """
        sql = text("""
                    update users
                    set username = COALESCE(:username, username),
                        password = COALESCE(:password, password)
                    where user_id = :user_id
                    returning user_id, email, username, created_at
                    """)
        result = self.db.execute(sql,{"user_id":user_id, "username":username, "password":password})
        self.db.commit()
        row = result.fetchone()
        return dict(row._mapping) if row else None

    def get_user_by_email(self, email: str) -> Optional[Tuple]:
        """
        이메일을 기반으로 사용자를 조회하여 튜플 형태로 반환합니다.
        """
        sql = text("""select user_id, username, email, password, created_at
                     from users
                     where email = (:email)
                  """)
        result = self.db.execute(sql,{"email":email})
        row = result.fetchone()
        return dict(row._mapping) if row else None

    def get_user_by_id(self, user_id: int) -> Optional[Tuple]:
        """
        유저 ID를 기반으로 사용자를 조회하여 튜플 형태로 반환합니다.
        """
        sql = text("""select user_id, username, email, password, created_at
                      from users
                      where user_id = (:user_id)
                    """)
        result = self.db.execute(sql,{"user_id":user_id})
        row = result.fetchone()
        return dict(row._mapping) if row else None

    def save_refresh_token(self, user_id: int, refresh_token: str) -> None:
        """
        로그인 시 Refresh Token 생성해서 DB에 저장
        """
        sql = text("""insert into refresh_tokens (user_id, token)
                      values (:user_id, :token)
                   """)
        result = self.db.execute(sql,{"user_id":user_id, "token":refresh_token})
        self.db.commit()

    def get_refresh_token(self, token: str) -> Optional[Tuple]:
        """
        DB에서 Refresh Token을 찾아서 유효한지 확인
        """
        sql = text("""select token 
                      from refresh_tokens 
                      where token = (:token)
                   """)
        result = self.db.execute(sql,{"token":token})
        row = result.fetchone()
        return dict(row._mapping) if row else None

    def delete_refresh_token(self, user_id: int, refresh_token: str) -> None:
        """
        로그아웃 시 DB에서 토큰 삭제
        """
        sql = text("""delete from refresh_tokens
                   where user_id = (:user_id)""")
        result = self.db.execute(sql,{"user_id":user_id})
        self.db.commit()