from dataclasses import dataclass
from typing import Optional

from aiohttp_session import Session
from sqlalchemy import Column, Integer, String

from app.store.database.sqlalchemy_base import db
from app.web.utils import hash_password


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None  # password_hash

    def is_password_valid(self, password: str) -> bool:
        return self.password == hash_password(password)

    @classmethod
    def from_session(cls, session: Optional[Session]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])


class AdminModel(db):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # password_hash

    def __repr__(self):
        return f"AdminModel(id={self.id}, email={self.email})"

    @property
    def dataclass(self) -> Admin:
        return Admin(id=self.id,
                     email=self.email,
                     password=self.password)
