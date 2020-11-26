import datetime as dt
import pprint as pp

from src.services import calculate_program_fulfillment_time

if __name__ == '__main__':
    nov26 = dt.date.today()

    data = calculate_program_fulfillment_time(500, nov26)

    for _, o in enumerate(data):
        pp.pprint({'№': _ + 1,
                   "Timestamp": o.timestamp_ns,
                   "Side": o.side.name,
                   "Price": o.price,
                   "Size": o.size})
