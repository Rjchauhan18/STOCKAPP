
import streamlit as st
import yfinance as yf
from Home import *
from patterns import patterns
import requests
import os
import sys
import subprocess
# import talib as ta

# check if the library folder already exists, to avoid building everytime you load the pahe
if not os.path.isdir("/tmp/ta-lib"):

    # Download ta-lib to disk
    with open("/tmp/ta-lib-0.4.0-src.tar.gz", "wb") as file:
        response = requests.get(
            "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        )
        file.write(response.content)
    # get our current dir, to configure it back again. Just house keeping
    default_cwd = os.getcwd()
    os.chdir("/tmp")
    # untar
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    # build
    os.system("./configure --prefix=/home/appuser/venv/")
    os.system("make")
    # install
    os.system("mkdir -p /home/appuser/venv/")
    os.system("make install")
    os.system("ls -la /home/appuser/venv/")
    # back to the cwd
    os.chdir(default_cwd)
    sys.stdout.flush()

# add the library to our current environment
from ctypes import *

lib = CDLL("/home/appuser/venv/lib/libta_lib.so.0.0.0")
# import library
try:
    import talib as ta
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--global-option=build_ext", "--global-option=-L/home/appuser/venv/lib/", "--global-option=-I/home/appuser/venv/include/", "ta-lib==0.4.24"])
finally:
    import talib as ta


st.header('**High ADX Company :**')






    #----------------------ADX INDICATOR------------------------------------------------#
    
def adx() :
    ADX_DIC ={}
    # company = Company_Name.values()
    # st.write(company)
    for stocks in company:
        # st.write(stocks)
        data_symbol = yf.Ticker(stocks)
        data = data_symbol.history(period=periods,interval=timeframes, start=start, end=end)
        data.rename(columns={'Open':'open','Close':'close','High':'high','Low':'low'}, inplace=True)
        ADX_VALUE = ta.ADX(data['high'],data['low'],data['close'],timeperiod=14)
        adx_result = ADX_VALUE.tail(1).values[0]
        if adx_result >25 :
            ADX_DIC[stocks] = adx_result
    SORTED_ADX_DIC = sorted(ADX_DIC.items(), key=lambda x: x[1], reverse=True)
    st.write(SORTED_ADX_DIC)
    macd_stocks = list(ADX_DIC.keys())
    macd(macd_stocks)
    
def pattern_reco(company_list):
    value = patterns.values()
    # st.write(value)
    Selected_pattern = st.selectbox('Select pattern', value)
    def key(selecte_pattern):
        for pattern,value in patterns.items() :
            if value == selecte_pattern:
                return pattern
            
    use_pattern = key(Selected_pattern)
    pattern_fun = getattr(ta, use_pattern)

    st.header('Company :')
    profit_stock = []
    for i in range (len(company_list)):
        # st.write(company_list[i])
        stock_data= yf.Ticker(company_list[i]) 

        data = stock_data.history(period='1d',interval=timeframes, start=start, end=end)
        data.rename(columns = {'Open' : 'open', 'High' : 'high', 'Low' : 'low', 'Close' : 'close', 'Volumn' : 'volumn'}, inplace = True)
        # main = "ta.{}(data['open'], data['high'], data['low'], data['close'])".formate(use_pattern)
        # st.write(main)
        # st.table(data)
        result = pattern_fun(data['open'], data['high'], data['low'], data['close'])
        # st.write(result)

        
        # result.rename(columns={' ' : 'Date',0:'detection'}, inplace=True)
        # st.write(result)
        last = result.tail(1).values[0]
    
        if last != 0:

            st.write(company_list[i])
            
            profit_stock.append(company_list[i])
    st.write(profit_stock)

    

MACD_BUY ={}
MACD_SELL ={}

def macd(stock_list) :

    for stocks in stock_list:
        data_symbol = yf.Ticker(stocks)
        data = data_symbol.history(period=periods,interval=timeframes, start=start, end=end)
        data.rename(columns={'Open':'open','Close':'close','High':'high','Low':'low'}, inplace=True)
        MACD_VALUE = ta.MACD(data['close'], fastperiod = 12, slowperiod = 26, signalperiod = 9)[0]
        
        macd_result = MACD_VALUE.tail(1).values[0]                                                       
        if macd_result <3.5 and macd_result>1:
            # value = stocks + ':' + adx_result
            MACD_BUY[stocks] = macd_result
        elif macd_result >-3.5 and macd_result < -1 :
            MACD_SELL[stocks] = macd_result

    #-----------------------MACD FINAL RESULT-----------------------------
        
    st.header("MACD buying stocks ")

    #-------------------------------------------MACD BUYING STOCKS---------------------------------------------------------------- 
    SORTED_MACD_BUY = sorted(MACD_BUY.items(), key=lambda x: x[1], reverse=True)
    st.write(SORTED_MACD_BUY)

    #------------------------------------------MACD SELLING STOCKS-----------------------------------------------------------------
    
    st.header("MACD selling stocks ")
    SORTED_MACD_SELL = sorted(MACD_SELL.items(), key=lambda x: x[1], reverse=True)
    st.write(SORTED_MACD_SELL)
    # st.write(MACD_BUY)
    find_stock = list(MACD_BUY.keys())
    
    pattern_reco(find_stock)

            


if __name__ == '__main__':
    adx()