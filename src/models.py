import enum
import time

from sqlalchemy import Column, Integer, BigInteger, Enum, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Side(enum.Enum):
    BUY = 0
    SELL = 1


class Order(Base):
    """
    Заказ
    """
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    timestamp_ns = Column(BigInteger, default=time.time_ns())
    side = Column(Enum(Side))
    price = Column(DECIMAL)
    size = Column(Integer)

    def __repr__(self):
        return f'<Order - account_id: {self.account_id} timestamp_ns: {self.timestamp_ns} ' \
               f'side: {self.side} price: {self.price}>'
