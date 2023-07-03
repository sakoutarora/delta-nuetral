from mibian import BS
import json
from datetime import datetime, timedelta
from dependencies.utils import gdata, DaysToExpire
from dependencies.constants import INTEREST_RATE
from dependencies.kitemanger import KiteManager
from dependencies.databasehandler import DataBaseManager

# init_managers 
ordermanger = KiteManager()
db = DataBaseManager()

#init vars
current_pos = None

def init(): 
    data = gdata()    # Fetch data 
    useful_data = {'data':[]}
    if data: 
        next_expiry = data['records']['expiryDates'][0]
        ordermanger.set_expiry(next_expiry)   # Setting exipry for orderManager 
        price_data = data['records']['data']
        for strike in price_data: 
            if strike['expiryDate'] == next_expiry:
                if 'CE' in strike:
                    underlyingPrice = strike['CE']['underlyingValue'] 
                    strikePrice = strike['CE']['strikePrice'] 
                    interestRate = INTEREST_RATE  
                    timeToExpiration = DaysToExpire(next_expiry)
                    volatility = strike['CE']['impliedVolatility'] 
                    bs = BS([underlyingPrice, strikePrice, interestRate, timeToExpiration], volatility)
                    delta = bs.callDelta
                    if delta:
                        strike['CE']['Delta'] = delta*100
                    
                if 'PE' in strike:
                    underlyingPrice = strike['PE']['underlyingValue'] 
                    strikePrice = strike['PE']['strikePrice'] 
                    interestRate = INTEREST_RATE  
                    timeToExpiration = DaysToExpire(next_expiry)
                    volatility = strike['PE']['impliedVolatility'] 
                    bs = BS([underlyingPrice, strikePrice, interestRate, timeToExpiration], volatility)
                    delta = bs.putDelta
                    if delta:
                        strike['PE']['Delta'] = delta*100
                useful_data['data'].append(strike)

        with open('datadump/data.json', 'w') as f: 
            f.write(json.dumps(useful_data))
    else:
        raise Exception("Couldn't read data")

def init_position(delta: int):
    # loading data 
    file = open('datadump/data.json', 'r')
    data = json.load(file)
    file.close()

    PE = []
    CE = []

    for strike in data['data']: 
        if 'CE' in strike:
            if 'Delta' in strike['CE']:
                CE.append((strike['CE']['strikePrice'], abs(strike['CE']['Delta'])))
        if 'PE' in strike:
            if 'Delta' in strike['PE']:
                PE.append((strike['PE']['strikePrice'], abs(strike['PE']['Delta'])))
    
    sPE = sorted(PE, key= lambda x: abs(x[1] - delta))[0]
    sCE = sorted(CE, key= lambda x: abs(x[1] - delta))[0]
    print(sPE, sCE)

    ordermanger.enter_position(sPE[0])
    ordermanger.enter_position(sCE[0])
    #update current postion and update TB


def CheckInitalPostion():
    # if any live postion for todays or not 
    global current_postion
    startstamp = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    current_postion = db.today_status(startstamp)
    print(current_postion)
    return current_postion

def TrackPos():
    pass