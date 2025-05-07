from dataclasses import dataclass
from fastapi import Depends
from core.db import get_db
from app.auth.models import User
from sqlalchemy import select
from sqlalchemy.orm import Session


@dataclass
class UserRepository:
    db: Session = Depends(get_db)

    def get_by_id(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
        return self.db.execute(query).scalars().first()

    def save(self, user: User) -> User:
        if user.id is None:
            self.db.add(user)

        self.db.commit()
        return user
