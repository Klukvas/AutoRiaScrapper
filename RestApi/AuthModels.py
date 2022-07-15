from sqlalchemy import Column, BigInteger, String, Boolean
from models import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    public_id = Column(BigInteger)
    name = Column(String)
    password = Column(String)
    admin = Column(Boolean)
