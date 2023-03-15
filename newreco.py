import yfinance as yf
import pandas as pd
import streamlit as st
import datetime as dt
import cufflinks as cf
# import matplotlib.pyplot as plt
# import plotly
import plotly.graph_objects as go
# import pandas_profiling
from streamlit_pandas_profiling import st_profile_report 
# from prophet import Prophet
from patterns import patterns
import talib as ta
# from talib import abstract



st.set_page_config(page_title="Stock Price Analysis" , page_icon=":bar_chart:", layout="wide")


st.markdown(
    """
        # Stock Price App\n
        Shown are the stock price data for the query companys!
    """
)
st.write('---')
from datetime import date
with st.sidebar:
    st.sidebar.markdown(' # Stock Price Analysis ')
    st.sidebar.title(f"Welcome ")
    start_date = st.sidebar.date_input("start date", dt.date(2023, 3, 15))
    End_date = st.sidebar.date_input("End date",dt.date(2023,3,16)) 

    # Retrieving tickers data
    ticker_list = ('TATASTEEL.NS', 'TCS.NS', 'HDFCLIFE.NS', 'WIPRO.NS', 'EICHERMOT.NS', 'INFY.NS', 'MARUTI.NS', 'TECHM.NS', 'BRITANNIA.NS', 'HCLTECH.NS', 'BAJAJ-AUTO.NS', 'SBIN.NS', 'HINDUNILVR.NS', 'DRREDDY.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'JSWSTEEL.NS', 'TATASTEEL.NS', 'NTPC.NS', 'POWERGRID.NS', 'COALINDIA.NS', 'BHARTIARTL.NS', 'SBILIFE.NS',
                'ONGC.NS', 'BAJFINANCE.NS', 'ULTRACEMCO.NS', 'SUNPHARMA.NS', 'ADANIENT.NS', 'LT.NS', 'BAJAJFINSV.NS', 'UPL.NS', 'ADANIPORTS.NS', 'CIPLA.NS', 'HINDALCO.NS', 'BPCL.NS', 'NESTLEIND.NS', 'KOTAKBANK.NS', 'HDFCBANK.NS', 'RELIANCE.NS', 'APOLLOHOSP.NS', 'HDFC.NS', 'DIVISLAB.NS', 'GRASIM.NS', 'TITAN.NS', 'ITC.NS', 'ASIANPAINT.NS', 'HEROMOTOCO.NS')
    
    # Select ticker symbol
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) 

    #period and timeframe
    periods_part,timeframes_part = st.columns(2)
    with periods_part:
        periods = st.sidebar.selectbox('Period', ('1d', '5d', '1y'))
    with timeframes_part:
        timeframes = st.sidebar.selectbox('Timeframe', ('1m', '5m', '15m', '30m', '1h', '2h', '4h'))

    #----------------------ADX INDICATOR------------------------------------------------#
    
    def adx() :
        ADX_DIC ={}
        for stocks in ticker_list:
            data_symbol = yf.Ticker(stocks)
            data = data_symbol.history(period=periods,interval=timeframes, start=start_date, end=End_date)
            data.rename(columns={'Open':'open','Close':'close','High':'high','Low':'low'}, inplace=True)
            ADX_VALUE = ta.ADX(data['high'],data['low'],data['close'],timeperiod=14)
            adx_result = ADX_VALUE.tail(1).values[0]
            if adx_result >25 :
                # value = stocks + ':' + adx_result
                ADX_DIC[stocks] = adx_result
                # # st.write(f"{stocks}     :       {adx_result}")
                # ADX_LIST.append(stocks)

        SORTED_ADX_DIC = sorted(ADX_DIC.items(), key=lambda x: x[1], reverse=True)
        st.write(SORTED_ADX_DIC)
            





    # Get ticker data
    tickerData = yf.Ticker(tickerSymbol) 

    #pandas profiling 
    navigation = st.radio('Navigation',['Home','Stock Report','Pattern Recognization','Range Of the day','Community']) 

# ---------------------------------------------------------HOME MENU :---------------------------------------------------

if navigation == 'Home' :



    # get the historical prices for this ticke
    tickerDf = tickerData.history(period=periods,interval=timeframes, start=start_date, end=End_date)
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
    #plot the graph
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
    st.header('**High ADX Company :**')
    adx()

    
    # -----------------------------------------------------Predict forecast with Prophet.
# # 
#     df_train = tickerDf[['Datetime','Close']]
#     df_train = df_train.rename(columns={"Datetime": "ds", "Close": "y"})

#     m = Prophet()
#     m.fit(df_train)
#     future = m.make_future_dataframe(periods=(start_date - End_date))
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
    tickerDf = tickerData.history(period='1d', start=start_date, end=End_date)
    tickerDf.reset_index(inplace=True)
    profiling = tickerDf.profile_report()
    st_profile_report(profiling)
#-------------------------------------------------------------------PATTERN RECOGNIZATION---------------------------------------------------
if navigation == 'Pattern Recognization' :
    value = patterns.values()
    # st.write(value)
    Selected_pattern = st.selectbox('Select pattern', value)
    def key(selecte_pattern):
        for pattern,value in patterns.items() :
            if value== selecte_pattern:
                return pattern
            
    use_pattern = key(Selected_pattern)
    pattern_fun = getattr(ta, use_pattern)

    st.header('Company :')
    profit_stock = []
    for i in range (len(ticker_list)):
        stock_data= yf.Ticker(ticker_list[i]) 

        data = stock_data.history(period='1d',interval=timeframes, start=start_date, end=End_date)
        data.rename(columns = {'Open' : 'open', 'High' : 'high', 'Low' : 'low', 'Close' : 'close', 'Volumn' : 'volumn'}, inplace = True)
        # st.table(data)
        result = pattern_fun(data['open'], data['high'], data['low'], data['close'])

        
        # result.rename(columns={' ' : 'Date',0:'detection'}, inplace=True)
        # st.write(result)
        last = result.tail(1).values[0]
       
        if last != 0:

            st.write(ticker_list[i])
            
            profit_stock.append(ticker_list[i])
            # st.write(result)
            # st.write(result.loc[result['0']==100])
    st.write(profit_stock)


    
#-------------------------------------------------------Range of the day ----------------------------------------------------------------------
if navigation == 'Range Of the day':
    st.write("Coming soon !")
#------------------------------------------------------Community-------------------------------------------------------------------------------
if navigation == 'Community':
    st.write("Coming soon!")

