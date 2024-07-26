from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Basket(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'basket'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    creator_id: int = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
