from sqlalchemy import Column, String, DateTime, Integer, BigInteger, Index
from app.core.db import Base


class PhoneData(Base):
    __tablename__ = 'phone_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String)
    start_date = Column(BigInteger)
    end_date = Column(BigInteger)


phone_hash_index = Index('idx_phone_hash', PhoneData.phone, postgresql_using='hash')


