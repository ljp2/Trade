import pytz
from datetime import datetime

def us_eastern_to_utc(us_eastern_time):
    us_eastern = pytz.timezone('US/Eastern')
    is_dst = us_eastern_time.dst()
    us_eastern_time = us_eastern.localize(us_eastern_time, is_dst=is_dst)
    utc_time = us_eastern_time.astimezone(pytz.utc)
    return utc_time

eastern_time = datetime(2024, 4, 2, 9,30, 0)  # Assuming it's in Eastern Daylight Time
utc_time = us_eastern_to_utc(eastern_time)
print("UTC Time:", utc_time)