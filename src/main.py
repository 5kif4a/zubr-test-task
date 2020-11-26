import datetime as dt

from src.services import calculate_program_fulfillment_time

if __name__ == '__main__':
    account_id = 500

    today = dt.date.today()

    part_of_day = calculate_program_fulfillment_time(account_id, today)

    print(f'{part_of_day * 100} per cent during this day, the client fulfilled the program conditions')
