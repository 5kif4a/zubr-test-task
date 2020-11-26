import random
import time

from src.db import session
from src.models import Side, Order


def fill_database():
    """
    Функция заполнения БД
    """
    for i in range(10 ** 6):
        account_id = random.randint(1, 1000)
        size = random.randint(0, 20)
        side = random.choice(list(Side))
        price = round(random.uniform(7.5, 15.5), 1)

        order = Order(account_id=account_id,
                      timestamp_ns=time.time_ns(),
                      side=side,
                      price=price,
                      size=size)

        session.add(order)

    session.commit()


fill_database()
