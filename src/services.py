import datetime as dt
import time

from sqlalchemy import and_, func

from src.constants import MM_SIZE, SPREAD
from src.db import session
from src.models import Order, Side


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


def get_orders_by_filter_condition(account_id: int, date: dt.date, side):
    begin_of_day = time.mktime(date.timetuple()) * 10 ** 9
    end_of_day = time.mktime((date + dt.timedelta(1)).timetuple()) * 10 ** 9

    condition = and_(Order.account_id == account_id,
                     Order.timestamp_ns.between(begin_of_day, end_of_day),
                     Order.size == MM_SIZE,
                     Order.side == side)

    return condition


def calculate_program_fulfillment_time(account_id: int, date: dt.date):
    """
    Функция, которая по заданному account_id маркет-мейкера и дате определяет,
    какую часть времени (доля) за эти сутки клиент выполнял условия программы.
    """
    program_fulfillment_time = 0

    buy_orders_condition = get_orders_by_filter_condition(account_id, date, Side.BUY)
    sell_orders_condition = get_orders_by_filter_condition(account_id, date, Side.SELL)

    min_sell_price = session.query(func.min(Order.price)).filter(sell_orders_condition).scalar()
    max_buy_price = session.query(func.max(Order.price)).filter(buy_orders_condition).scalar()

    spread = calculate_spread(min_sell_price, max_buy_price)

    if spread < SPREAD:
        sell_orders = session.query(Order).filter(Order.price == min_sell_price,
                                                  Order.side == Side.SELL,
                                                  Order.account_id == account_id)

        buy_orders = session.query(Order).filter(Order.price == max_buy_price,
                                                 Order.side == Side.BUY,
                                                 Order.account_id == account_id)

        program_fulfillment_time = (sell_orders.count() + buy_orders.count()) / (86400 * (10 ** 9))

    return program_fulfillment_time
