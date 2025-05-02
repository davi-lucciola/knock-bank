import logging
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from knockbankapi.domain.errors import InfraError
from knockbankapi.domain.models import User


@dataclass
class UserRepository:
    db: SQLAlchemy

    def get_by_id(self, id: int) -> User | None:
        return self.db.session.query(User).get(id)

    def get_by_token(self, token: str) -> User | None:
        return self.db.session.query(User).where(User.token == token).first()

    def save(self, user: User) -> User:
        try:
            if user.id is None:
                self.db.session.add(user)

            self.db.session.commit()
            return user
        except Exception as err:
            logging.error(err)
            self.db.session.rollback()
            raise InfraError('Houve um error ao salvar o usuario.')
