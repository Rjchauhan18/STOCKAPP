import yfinance as yf
import pandas as pd
import streamlit as st
import datetime as dt
import cufflinks as cf
# import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
# import pandas_profiling
from streamlit_pandas_profiling import st_profile_report 
# from prophet import Prophet
from patterns import patterns,Company_Name
# import talib as ta
# from talib import abstract
# import smtplib as smt 
# import streamlit as st
import requests
import os
import sys
import subprocess

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
    import talib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--global-option=build_ext", "--global-option=-L/home/appuser/venv/lib/", "--global-option=-I/home/appuser/venv/include/", "ta-lib==0.4.24"])
finally:
    import talib


st.set_page_config(page_title="Stock Price Analysis" , page_icon=":bar_chart:", layout="wide")


st.markdown(
    """
        # Stock Price App\n
        Shown are the stock price data for the query companys!
    """
)
st.write('---')



#----------------------------------------------------------------Email sender --------------------------------

# def email_sender (sender_email,sender_email_id_password, receiver_email):
#     s = smt.SMTP('smtp.gmail.com', 587)

#     s.starttls()

#     s.login(sender_email, sender_email_id_password)

#     message = "HI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

#     s.sendmail(sender_email, receiver_email,message)

#     s.quit()

# email_sender('rjchauhan@5000000gmail.com', 'Rjchauhan@18', 'rjchauhan@5000000gmail.com')








with st.sidebar:
    st.sidebar.markdown(' # Stock Price Analysis ')
    st.sidebar.title(f"Welcome ")

    start_date = dt.date.today()
    end_date = dt.date.today() + dt.timedelta(days=1)


    start= st.sidebar.date_input("start date", start_date)
    End = st.sidebar.date_input("End date", end_date) 

    # company = ('ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'HDFC.NS', 'ICICIBANK.NS', 'ITC.NS', 'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS', 'POWERGRID.NS',  'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAMTRDVR.NS',  'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'WIPRO.NS')

    # problem_list = ['AIRTELPP.NS','RELIANCEP1.NS','TATASTLPP.NS',]

    company = list(Company_Name.values())





    companies = Company_Name.keys()
    # st.write(company)

    # Select ticker symbol
    Symbol = st.sidebar.selectbox('Stock ticker', companies) 
    tickerSymbol = Company_Name.get(Symbol)

    #period and timeframe
    periods_part,timeframes_part = st.columns(2)
    with periods_part:
        periods = st.sidebar.selectbox('Period', ('1d', '5d', '1y'))
    with timeframes_part:
        timeframes = st.sidebar.selectbox('Timeframe', ('1m', '5m', '15m', '30m', '1h', '2h', '4h'))


      



    # Get ticker data
    tickerData = yf.Ticker(tickerSymbol) 

    #pandas profiling 
    navigation = st.radio('Navigation',['Home','Stock Report','Pattern Recognization','Range Of the day','Community']) 





    #----------------------ADX INDICATOR------------------------------------------------#
    
def adx() :
    ADX_DIC ={}
    # company = Company_Name.values()
    # st.write(company)
    for stocks in company:
        # st.write(stocks)
        data_symbol = yf.Ticker(stocks)
        data = data_symbol.history(period=periods,interval=timeframes, start=start_date, end=end_date)
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

        data = stock_data.history(period='1d',interval=timeframes, start=start_date, end=end_date)
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
        data = data_symbol.history(period=periods,interval=timeframes, start=start_date, end=end_date)
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

            









# ---------------------------------------------------------HOME MENU :---------------------------------------------------

if navigation == 'Home' :



    # get the historical prices for this ticke
    tickerDf = tickerData.history(period=periods,interval=timeframes, start=start_date, end=end_date)
    tickerDf.reset_index(inplace=True)

    # #coverting time zone to date :
    # tickerDf['Year'] = tickerDf['Date'].apply(lambda x:str(x)[-4:])
    # tickerDf['Month'] = tickerDf['Date'].apply(lambda x:str(x)[-6:-4:])
    # tickerDf['Day'] = tickerDf['Date'].apply(lambda x:str(x)[-6:])
    # tickerDf['date'] = pd.DataFrame(tickerDf['Year'] +'-' +tickerDf['Month'] +'-' + tickerDf['Day'])

    st.header('**Stock data**')
    st.table(tickerDf)

    
    # dividends
    # dividends = tickerDf.Dividends
    dividend,download = st.columns(2)
    with dividend :
      if st.button('BOLLINGER BAND'):
        # Bollinger bands
        st.header('**Bollinger Bands**')
        qf = cf.QuantFig(tickerDf, title='First Quant Figure',
                        legend='top', name='GS')
        qf.add_bollinger_bands()
        fig = qf.iplot(asFigure=True)
        st.plotly_chart(fig)
    with download:
        # download csv
        @st.cache
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        csv = convert_df(tickerDf)
        download = st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='stock.csv',
            mime='text/csv',
        )
    # plot the graph
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter( x=tickerDf['Datetime'], y=tickerDf['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(
            x=tickerDf['Datetime'], y=tickerDf['Close'], name="stock_close"))
        fig.layout.update(
            title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig , use_container_width=True)
    plot_raw_data()
    # ADX_LIST = []
    # macd(company)

    
    # -----------------------------------------------------Predict forecast with Prophet.
# # 
#     df_train = tickerDf[['Datetime','Close']]
#     df_train = df_train.rename(columns={"Datetime": "ds", "Close": "y"})

#     m = Prophet()
#     m.fit(df_train)
#     future = m.make_future_dataframe(periods=(start_date - end_date))
#     forecast = m.predict(future)

#     # Show and plot forecast
#     st.subheader('Forecast data')
#     st.write(forecast.tail())
#     n_years = st.slider('Years of prediction:', 1, 4)
#     period = n_years * 365
#     st.write(f'Forecast plot for {n_years} years')
#     fig1  = m.plot(forecast)
#     st.plotly_chart(fig1)

#     st.write("Forecast components")
#     fig2 = m.plot_components(forecast)
#     st.write(fig2)
#describe the bollinger band on the graph
  
# -------------------------------------------------------------PROFILING THE STOCK DATA : -------------------------------------------------------------------
if  navigation == 'Stock Report' :

    # get the historical prices for this ticke
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    tickerDf.reset_index(inplace=True)
    profiling = tickerDf.profile_report()
    st_profile_report(profiling)
#-------------------------------------------------------------------PATTERN RECOGNIZATION---------------------------------------------------
if navigation == 'Pattern Recognization' :
    
    st.header('**High ADX Company :**')
    adx()
    
    # pattern_reco(company)
    
  


    
#-------------------------------------------------------Range of the day ----------------------------------------------------------------------
if navigation == 'Range Of the day':
    st.write("Coming soon !")
#------------------------------------------------------Community-------------------------------------------------------------------------------
if navigation == 'Community':
    st.write("Coming soon!")

