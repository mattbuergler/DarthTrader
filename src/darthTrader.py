#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 16:09:08 2020

@author: MatthiasBuergler
"""
import numpy as np
import sys
import json
import requests
import time
import hmac
import hashlib
import math
from datetime import datetime

URL = 'https://api.crypto.com/v2/'
STATUS_CODE_OK = 200

def requestGET(method):
    try:
        res = requests.get(URL + method)
        if not (res.status_code == STATUS_CODE_OK):
            print("Last method:")
            print(method)
        res.raise_for_status()
    # except requests.exceptions.HTTPError as httpErr:
    #     raise SystemExit(httpErr)
    # except requests.exceptions.Timeout:
    #     print("Connection timed out.")
    # except requests.exceptions.TooManyRedirects:
    #     print("Too many redirects. Please check the URL.")
    except requests.exceptions.RequestException as requestE:
        # catastrophic error. bail.
        raise SystemExit(requestE)
    return res

def requestPOST(method, request):
    try:
        res = requests.post(URL + method, json=request)
        if not (res.status_code == STATUS_CODE_OK):
            print("Last method:")
            print(method)
            print("Last request:")
            print(request)
        res.raise_for_status()
    # except requests.exceptions.HTTPError as httpErr:
    #     raise SystemExit(httpErr)
    # except requests.exceptions.Timeout:
    #     print("Connection timed out.")
    # except requests.exceptions.TooManyRedirects:
    #     print("Too many redirects. Please check the URL.")
    except requests.exceptions.RequestException as requestE:
        # catastrophic error. bail.
        raise SystemExit(requestE)
    return res

def generateSignature(method,params, ID):
    API_KEY = "gH9rDJUgonXNHWiRc1Z8wH"
    f = open('DarthTrader.txt', 'r')
    l1 = f.readline()
    l2 = f.readline()
    SECRET_KEY = l2.split()[1].strip()
    # First ensure the params are alphabetically sorted by key
    request = {
      "id": ID,
      "method": method,
      "api_key": API_KEY,
      "params": params,
      "nonce": int(time.time() * 1000)
    };
    # First ensure the params are alphabetically sorted by key
    paramString = ""

    if "params" in request:
        keys = request['params'].keys()
        keyList = []
        for k in keys:
            keyList.append(k)
        keyList.sort()
        for key in keyList:
            paramString += key
            paramString += str(request['params'][key])

    sigPayload = request['method'] + str(request['id']) + request['api_key'] + paramString + str(request['nonce'])

    request['sig'] = hmac.new(
      bytes(str(SECRET_KEY), 'utf-8'),
      msg=bytes(sigPayload, 'utf-8'),
      digestmod=hashlib.sha256
    ).hexdigest()
    return request

def getInstruments():
    method = 'public/get-instruments'
    return requestGET(method)

def getTicker(instrument_name):
    method = 'public/get-ticker?instrument_name=' + instrument_name
    return requestGET(method)

def getCandleSticks(instrument_name, timeframe):
    method = 'public/get-candlestick?instrument_name=' + instrument_name + "&timeframe=" + timeframe
    return requestGET(method)

def getCandleLastClose(instrument_name, timeframe):
    res = getCandleSticks(instrument_name=instrument_name, timeframe=timeframe)
    data = res.json()['result']['data']
    # convert to numpy array
    dataCandle = []
    for d in data:
      dataCandle.append(np.asarray(list(d.values())))
    dataCandle = np.asarray(dataCandle)
    return dataCandle[-1,4]

def getCandleLastOpen(instrument_name, timeframe):
    res = getCandleSticks(instrument_name=instrument_name, timeframe=timeframe)
    data = res.json()['result']['data']
    # convert to numpy array
    dataCandle = []
    for d in data:
      dataCandle.append(np.asarray(list(d.values())))
    dataCandle = np.asarray(dataCandle)
    return dataCandle[-1,1]

def getCandleLastLow(instrument_name, timeframe):
    res = getCandleSticks(instrument_name=instrument_name, timeframe=timeframe)
    data = res.json()['result']['data']
    # convert to numpy array
    dataCandle = []
    for d in data:
      dataCandle.append(np.asarray(list(d.values())))
    dataCandle = np.asarray(dataCandle)
    return dataCandle[-1,3]

def getCandleLastHigh(instrument_name, timeframe):
    res = getCandleSticks(instrument_name=instrument_name, timeframe=timeframe)
    data = res.json()['result']['data']
    # convert to numpy array
    dataCandle = []
    for d in data:
      dataCandle.append(np.asarray(list(d.values())))
    dataCandle = np.asarray(dataCandle)
    return dataCandle[-1,2]

def getCandleLastTime(instrument_name, timeframe):
    res = getCandleSticks(instrument_name=instrument_name, timeframe=timeframe)
    data = res.json()['result']['data']
    # convert to numpy array
    dataCandle = []
    for d in data:
      dataCandle.append(np.asarray(list(d.values())))
    dataCandle = np.asarray(dataCandle)
    return dataCandle[-1,0]

def getCandleLastVolume(instrument_name, timeframe):
    res = getCandleSticks(instrument_name=instrument_name, timeframe=timeframe)
    data = res.json()['result']['data']
    # convert to numpy array
    dataCandle = []
    for d in data:
      dataCandle.append(np.asarray(list(d.values())))
    dataCandle = np.asarray(dataCandle)
    return dataCandle[-1,5]

# fetches the price of the latest trade
def getTickerPrice(instrument_name):
    res = getTicker(instrument_name=instrument_name) 
    items = res.json()
    return items['result']['data']['a']

# fetches the timestamp of the latest trade
def getTickerTime(instrument_name):
    res = getTicker(instrument_name=instrument_name) 
    items = res.json()
    return items['result']['data']['t']

def getAccountSummary(ID):
    method = "private/get-account-summary"
    params = {}
    request = generateSignature(method=method, params=params, ID=ID)
    return requestPOST(method=method, request=request)

def createOrder(ID, instrument_name, side, orderType, price=None, quantity=None, client_oid=None, time_in_force=None, exec_inst=None):
    method = 'private/create-order'
    params = {'instrument_name': instrument_name,
          'side': side,
          'type': orderType}
    if not price == None:
        params['price'] = price
    if not quantity == None:
        params['quantity'] = quantity
    if not client_oid == None:
        params['client_oid'] = client_oid
    if not time_in_force == None:
        params['time_in_force'] = time_in_force
    if not exec_inst == None:
        params['exec_inst'] = exec_inst
    request = generateSignature(method=method, params=params, ID=ID)
    return requestPOST(method=method, request=request)


def getOpenOders(ID, instrument_name=None):
    method = 'private/get-open-orders'
    if not instrument_name == None:
        params = {"instrument_name": instrument_name}
    else:
        params = {}
    request = generateSignature(method=method, params=params, ID=ID)
    return requestPOST(method=method, request=request)

def haveOpenOder(ID, instrument_name=None):
    if not instrument_name == None:
        res = getOpenOders(ID=ID, instrument_name=instrument_name)
    else:
        res = getOpenOders(ID=ID)
    nOpenOrders = res.json()['result']['count']
    if (nOpenOrders == 0):
        return False
    else:
        return True

def getOpenOderStatus(ID, instrument_name):
    res = getOpenOders(ID=ID, instrument_name=instrument_name)
    # take uppermost order so far, assuming only one order at a time
    openOrders = res.json()['result']['order_list'][0]
    return openOrders['status']



def getOderHistory(ID, instrument_name=None, start_ts=None, end_ts=None, page_size=None, page=None):
    method = 'private/get-order-history'
    params = {}
    if not instrument_name == None:
        params['instrument_name'] = instrument_name
    if not start_ts == None:
        params['start_ts'] = start_ts
    if not end_ts == None:
        params['end_ts'] = end_ts
    if not page_size == None:
        params['page_size'] = page_size
    if not page == None:
        params['page'] = page
    request = generateSignature(method=method, params=params, ID=ID)
    return requestPOST(method=method, request=request)

def PRINTERROR(error_msg):
    print(error_msg)
    print('Dath Trader has been killed...')
    sys.exit()

def PRINTLOGO():
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$                                                                          $")
    print("$     ___   __     ___  ____          ____  ___   __     ___   ____ ___    $")
    print("$    /   / /  |   /   /  /   /   /     /   /   / /  |   /   / /    /   /   $")
    print("$   /   / /---|  /---   /   /---/     /   /---  /---|  /   / /--- /---     $")
    print("$  /___/ /    | / \\    /   /   /     /   / \\   /    | /___/ /___ / \\       $")
    print("$                                                                          $")
    print("$                                                                          $")
    print("$  © 2020 Matthias Buergler                                                $")
    print("$                                                                          $")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("")

def printDataPair(name, data):
    print("-> "+name + str(data))


class Wallet:
    """This is the wallet"""

    def __init__(self):
        res = getAccountSummary(ID=0)
        summary = res.json()['result']['accounts']
        acc = {}
        for token in summary:
            coin = token['currency']
            del token['currency']
            acc[coin] = token
        self.account = acc

    def update(self):
        res = getAccountSummary(ID=0)
        summary = res.json()['result']['accounts']
        acc = {}
        for token in summary:
            coin = token['currency']
            del token['currency']
            acc[coin] = token
        self.account = acc

    def getBalance(self, coin):
        return self.account[coin]['balance']

    def getAvailable(self, coin):
        return self.account[coin]['available']

    def getOrder(self, coin):
        return self.account[coin]['order']

    def getStake(self, coin):
        return self.account[coin]['stake']

    def printCoinStatement(self, coin):
        print('Wallet statement: ' + coin)
        printDataPair('Balance:   ', myWallet.getBalance(coin))
        printDataPair('Available: ', myWallet.getAvailable(coin))
        printDataPair('Order:     ', myWallet.getOrder(coin))
        printDataPair('Stake:     ', myWallet.getStake(coin))
        print('')


    def placeLimitBuyOrder(self, ID, instrument_name, price, quantity, oid=None):
        side = 'BUY'
        orderType = 'LIMIT'
        return createOrder(ID=ID, instrument_name=instrument_name, side=side, orderType=orderType, price=price, quantity=quantity, client_oid=oid)

    def placeLimitSellOrder(self, ID, instrument_name, price, quantity, oid=None):
        side = 'SELL'
        orderType = 'LIMIT'
        return createOrder(ID=ID, instrument_name=instrument_name, side=side, orderType=orderType, price=price, quantity=quantity, client_oid=oid)


if __name__ == "__main__":
    #----------------------------------------#
    # Some data to define by the user:       #
    #----------------------------------------#
    # the instrument name
    instrument = "DAI_CRO"
    # the cost that should be covered by a buy/sell order [main coin value], e.g. 0.0008 Cro
    min_trading_cost = 0.0
    # maximum trading duration [s]
    max_trading_duration = 24*3600
    # intitial trading quantity of the main coin
    mainInitTradingQuantity = 100
    # set maximum price for initial buy
    maxInitPrice = 5.6
    # do we have to buy the trade currency first?
    buyFirst = True

    ## currently always assuming that we buy first!!!!

    #----------------------------------------#
    # Initializing the bot...                #
    #----------------------------------------#
    PRINTLOGO()
    # define and initialize some variables
    myWallet = Wallet()
    mainCoin = instrument.split('_')[1]   # should be CRO, BTC, USTD
    tradeCoin = instrument.split('_')[0]  # can be any coin

    mainBal = myWallet.getBalance(mainCoin)
    tradeBal = myWallet.getBalance(tradeCoin)

    # print some initial data
    printDataPair('Instrument: ', instrument)
    printDataPair('Main coin:  ', mainCoin)
    printDataPair('Trade coin: ', tradeCoin)
    print('')

    myWallet.printCoinStatement(mainCoin)
    myWallet.printCoinStatement(tradeCoin)

    # initialize some trading variables
    requestID = 0
    orderID = 0
    nBuys = 0
    nSells = 0
    if (buyFirst):
        BUY = True
        SELL = False
    else:
        BUY = False
        SELL = True

    # get candle sticks for last closing price for 1m timeframe
    timeFrame = '1m'
    pClose = getCandleLastOpen(instrument_name=instrument, timeframe=timeFrame)

    # set current min and max
    pMin = 0.0
    pMax = pClose

    # set up trading balances
    if (myWallet.getAvailable(mainCoin) >= mainInitTradingQuantity):
        mainTradingQuantity = mainInitTradingQuantity
    else:
        PRINTERROR("Initial trading quantity < available quantity.")
    tradeTradingQuantity= 0.0
    mainInitQuantity = myWallet.getBalance(mainCoin) - mainInitTradingQuantity

    #----------------------------------------#
    # Starting the bot...                    #
    #----------------------------------------#
    # start timing in milliseconds since the Unix epoch
    t_start = time.time()*1000
    t_current = t_start
    t_end = t_start + (max_trading_duration * 1000)

    #### TEST SECTION ##### 
    # p = getTickerPrice(instrument_name=instrument)
    # res = getOpenOders(ID=orderID, instrument_name=instrument)
    # sys.exit() 
    #######################

    print("")
    printDataPair('Starting time (UTC): ', datetime.utcfromtimestamp(int(round(t_start/1000.0))).strftime('%Y-%m-%d %H:%M:%S'))
    print("Run Darth Trader! Run!")
    print("")
    # start time loop
    while(t_current <= t_end):
        printDataPair("Time running [h]:     ",(t_current - t_start)/1000.0/3600.0)
        printDataPair("Number of trades: ",nBuys+nSells)
        myWallet.update()
        myWallet.printCoinStatement(mainCoin)
        myWallet.printCoinStatement(tradeCoin)
        # check if we have an open order
        res = getOpenOders(ID=orderID, instrument_name=instrument)
        requestID+=1
        if (res.json()['result']['count'] == 0):
            haveOpenOrder = False
        else: 
            haveOpenOrder = True
        if not (haveOpenOrder):
            # check if we want to sell or buy
            print('Sell or buy or die...')
            # for actual run! deactive for dry run
            mainTradingQuantity = myWallet.getBalance(mainCoin) - mainInitQuantity
            tradeTradingQuantity =myWallet.getAvailable(tradeCoin)
            if BUY:
                # we are trying to buy...
                # get current ticker price
                p = getTickerPrice(instrument_name=instrument)
                printDataPair('Current price:  ', p)
                # track min/max price
                pMax = max(p,pMax)
                pMin = min(p,pMin)
                if ((nBuys > 0) & (p > pMin)):
                    gain = ((mainTradingQuantity/p)-(mainTradingQuantity/pLast))/(mainTradingQuantity/p)
                    printDataPair('gain by buy', gain)
                    if (gain > min_trading_cost):
                        if (myWallet.getAvailable(mainCoin) >= mainTradingQuantity):
                            printDataPair('Time:       ', datetime.utcfromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d %H:%M:%S'))
                            printDataPair('Buying at:  ', p)
                            # simulation
                            # tradeTradingQuantity += mainTradingQuantity / p
                            # mainTradingQuantity -= mainTradingQuantity
                            # place actual oder
                            quantity = math.floor(mainTradingQuantity/p*100)/100.0
                            res = myWallet.placeLimitBuyOrder(ID=requestID, instrument_name=instrument, price=p, quantity=quantity, oid=orderID)
                            orderID += 1
                            requestID+=1
                            pLast = p
                            pMax = p
                            BUY = False
                            SELL = True
                            nBuys += 1
                        else:
                            PRINTERROR("Not enough " + mainCoin + "s to buy.")
                # check if initial buy and price is below max initial price
                elif ((nBuys == 0) & (p <= maxInitPrice)):
                    if (myWallet.getAvailable(mainCoin) >= mainTradingQuantity):
                        printDataPair('Time:       ', datetime.utcfromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d %H:%M:%S'))
                        printDataPair('Buying at:  ', p)
                        # simulation
                        # tradeTradingQuantity += mainTradingQuantity / p
                        # mainTradingQuantity -= mainTradingQuantity
                        # place actual oder
                        quantity = math.floor(mainTradingQuantity/p*100)/100.0
                        res = myWallet.placeLimitBuyOrder(ID=requestID, instrument_name=instrument, price=p, quantity=quantity, oid=orderID)
                        orderID += 1
                        requestID+=1
                        pLast = p
                        pMax = p
                        BUY = False
                        SELL = True
                        nBuys += 1
                    else:
                        PRINTERROR("Not enough " + mainCoin + "s to buy.")
            elif SELL:
                # we want to sell this shit!
                # get current ticker price
                p = getTickerPrice(instrument_name=instrument)
                printDataPair('Current price:  ', p)
                # track min/max price
                pMax = max(p,pMax)
                pMin = min(p,pMin)
                if ((p < pMax)):
                    gain = ((tradeTradingQuantity*p)-(tradeTradingQuantity*pLast))/(tradeTradingQuantity*p)
                    printDataPair('gain by sell:  ', gain)
                    if (gain > min_trading_cost):
                        if (myWallet.getAvailable(tradeCoin) >= tradeTradingQuantity):
                            printDataPair('Time:       ', datetime.utcfromtimestamp(int(round(time.time()))).strftime('%Y-%m-%d %H:%M:%S'))
                            printDataPair('Selling at: ', p)
                            # mainTradingQuantity += tradeTradingQuantity * p
                            # tradeTradingQuantity -= tradeTradingQuantity
                            # place actual oder
                            res = myWallet.placeLimitSellOrder(ID=requestID, instrument_name=instrument, price=p, quantity=tradeTradingQuantity, oid=orderID)
                            orderID += 1
                            requestID+=1
                            pLast = p
                            BUY = True
                            SELL = False
                            nBuys += 1
                            pMin = p
                        else:
                            PRINTERROR("Not enough " + tradeCoin + "s to sell.")
        else:
            # we have an open order
            orderStatus = res.json()['result']['order_list'][0]['status']
            if orderStatus == 'ACTIVE':
                ## implement check for if price is reasonable
                print("Order is active...")
                p = getTickerPrice(instrument_name=instrument)
                printDataPair('Current price:  ', p)
            else:
                PRINTERROR("Order status for order XZY is not ACTIVE.")
        time.sleep(.5)
        t_current = time.time()*1000
    print('finished trading...')
