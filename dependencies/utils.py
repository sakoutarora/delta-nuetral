import requests
import json
from datetime import datetime, timedelta
import calendar
from dependencies.constants import OPTION_CHAIN_END_POINT

def gdata():
    headers = {
        'User-Agent': 'PostmanRuntime/7.32.2',
        'Connection': 'keep-alive'
    }
    resp = requests.get(OPTION_CHAIN_END_POINT, headers=headers)
    if resp:
        return resp.json()
    else:
        return None


def get_strike_info(StrikePrice, expiry, option):
    with open('data.json', 'r') as f:
        data = json.load(f)
    for strike in data['data']:
        if strike['strikePrice'] == StrikePrice:
            return strike[option]

def DaysToExpire(next_expiry:str):
    expiry = datetime.strptime(next_expiry, '%d-%b-%Y')
    curdate = datetime.now()
    return (expiry - curdate).days

def is_non_emplty_list(array:list) -> bool:
    return (len(array) > 0)
