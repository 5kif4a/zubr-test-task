import datetime as dt
import time

from sqlalchemy import and_

from src.db import session
from src.models import Order


def calculate_spread(min_sell_price: float, max_buy_price: float) -> float:
    """
    Функция, рассчитывающия SPREAD
    :param min_sell_price: минимальная цена продажи
    :param max_buy_price: максимальная цена покупки
    :return: float
    """
    avg_price = (min_sell_price + max_buy_price) / 2
    spread = (max_buy_price - min_sell_price) / avg_price * 10000

    return spread


def calculate_program_fulfillment_time(account_id: int, date: dt.date):
    """
    Функция, которая по заданному account_id маркет-мейкера и дате определяет,
    какую часть времени (доля) за эти сутки клиент выполнял условия программы.
    """

    begin_of_day = time.mktime(date.timetuple()) * 10 ** 9
    end_of_day = time.mktime((date + dt.timedelta(1)).timetuple()) * 10 ** 9

    condition = and_(Order.account_id == account_id,
                     Order.timestamp_ns.between(begin_of_day, end_of_day))

    orders = session.query(Order).filter(condition)



    return orders
