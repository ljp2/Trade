from datetime import datetime
import pytz

def convert_to_utc(year, month, day, hour, minute):
    nyc_tz = pytz.timezone('America/New_York')
    utc_tz = pytz.timezone('UTC')
    nyc_time = nyc_tz.localize(datetime(year, month, day, hour, minute))
    utc_time = nyc_time.astimezone(utc_tz)
    return int(utc_time.timestamp())

def convert_to_nyc(utc_timestamp):
    utc_tz = pytz.timezone('UTC')
    nyc_tz = pytz.timezone('America/New_York')
    utc_time = datetime.fromtimestamp(utc_timestamp, tz=utc_tz)
    nyc_time = utc_time.astimezone(nyc_tz)
    return nyc_time
