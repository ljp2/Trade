import requests
import json
import datetime
import pytz

# Disable SSL Warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def contractSearch():
    base_url = "https://localhost:5000/v1/api/"
    endpoint = "iserver/secdef/search"
    json_body = {'symbol': 'SPY', 'secType': 'STK', 'name': False}
    contract_req = requests.post(url=base_url + endpoint, json=json_body, verify=False)
    contract_json = json.dumps(contract_req.json(), indent=2)
    print(contract_json)


def contractInfo():
    base_url = "https://localhost:5000/v1/api/"
    endpoint = "iserver/secdef/info"
    conid="conid=11004968"
    secType="secType=FUT"
    month="month=JUN24"
    exchange="exchange=CME"
    params = "&".join([conid, secType, month, exchange])
    request_url = "".join([base_url, endpoint, "?", params])
    contract_req = requests.get(url=request_url, verify=False)
    contract_json = json.dumps(contract_req.json(), indent=2)
    print(contract_req)
    print(contract_json)


def marketSnapshot():
    base_url = "https://localhost:5000/v1/api/"
    endpoint = "iserver/marketdata/snapshot"
    conid = "conids=11004968, 237937002"
    fields = "fields=31,55,84,86"
    params = "&".join([conid, fields])
    request_url = "".join([base_url, endpoint, "?", params])
    contract_req = requests.get(url=request_url, verify=False)
    contract_json = json.dumps(contract_req.json(), indent=2)
    print(contract_req)
    print(contract_json)

def historicalData():
    local_time = datetime.datetime(2024, 3, 27, 9, 30, 0)
    local_timezone = pytz.timezone('America/New_York')
    local_time_with_tz = local_timezone.localize(local_time)
    utc_time = local_time_with_tz.astimezone(pytz.utc)


    base_url = "https://localhost:5000/v1/api/"
    endpoint = "/hmds/history"
    # endpoint = "/iserver/marketdata/history"
    conid = "conid=265598"
    period = "period=1w"
    bar = "bar=1d"
    outsideRth = "outsideRth=true"
    # direction = "direction=-1"
    # startTime = f"startTime={utc_time.strftime('%Y%m%d-%H:%M:%S')}"
    # startTime = "startTime=20230821-13:30:00"

    barType = "barType=midpoint"
    
    params = "&".join([conid, period, bar, outsideRth, barType])
    request_url = "".join([base_url, endpoint, "?", params])
    contract_req = requests.get(url=request_url, verify=False)
    contract_json = json.dumps(contract_req.json(), indent=2)
    print(contract_req)
    print(contract_json)

def check():
    base_url = "https://localhost:5000/v1/api/"
    endpoint = "/iserver/auth/status"
    request_url = "".join([base_url, endpoint])
    contract_req = requests.get(url=request_url, verify=False)
    contract_json = json.dumps(contract_req.json(), indent=2)
    print(contract_req)
    print(contract_json)

if __name__ == "__main__":
    historicalData()


    