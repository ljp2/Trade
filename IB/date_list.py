from datetime import datetime, timedelta, date

def get_weekdays(start_date, end_date):
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()
    weekdays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
            weekdays.append(current_date)
        current_date += timedelta(days=1)
    return weekdays

def format_dates(date_list):
    formatted_dates = []
    for date_obj in date_list:
        formatted_date = date_obj.strftime("%Y%m%d 23:59:00 US/Eastern")
        formatted_dates.append(formatted_date)
    return formatted_dates

if __name__ == "__main__":
    start_date = date(2024, 3, 1)
    end_date = date(2024, 3, 31)
    weekdays = get_weekdays(start_date, end_date)
    for x in format_dates(weekdays):
        print(x)


