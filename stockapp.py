import yfinance as yf
import pandas as pd
import streamlit as st
import datetime as dt
import cufflinks as cf
import matplotlib.pyplot as plt


#app title
st.markdown(
    """
    # Stock Price Analysis \n
    Shown are the stock price data for the query companys!

    """
)

st.write('---')

#sidebar
st.sidebar.subheader('Query parameter')
start_date = st.sidebar.date_input("start date", dt.date(2021,1,1))
End_date = st.sidebar.date_input("End date", dt.date(2022,1,1))

# Retrieving tickers data
ticker_list = ('TATASTEEL.NS','TCS.NS','HDFCLIFE.NS','WIPRO.NS','EICHERMOT.NS','INFY.NS','MARUTI.NS','TECHM.NS','BRITANNIA.NS','HCLTECH.NS','MM.NS','BAJAJ-AUTO.NS','SBIN.NS','HINDUNILVR.NS','DRREDDY.NS','ICICIBANK.NS','INDUSINDBK.NS','JSWSTEEL.NS','TATASTEEL.NS','NTPC.NS','POWERGRID.NS','COALINDIA.NS','BHARTIARTL.NS','SBILIFE.NS','ONGC.NS','BAJFINANCE.NS','ULTRACEMCO.NS','SUNPHARMA.NS','ADANIENT.NS','LT.NS','BAJAJFINSV.NS','UPL.NS','ADANIPORTS.NS','CIPLA.NS','HINDALCO.NS','BPCL.NS','NESTLEIND.NS','KOTAKBANK.NS','HDFCBANK.NS','RELIANCE.NS','APOLLOHOSP.NS','HDFC.NS','DIVISLAB.NS','GRASIM.NS','TITAN.NS','ITC.NS','ASIANPAINT.NS','HEROMOTOCO.NS')

tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=End_date) #get the historical prices for this ticke

# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

#for getting companys full name
string_name = tickerData.info['longName']
st.header('**%s**' % string_name)


# for getting information of company
string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)

# Ticker data
st.header('**Ticker data**')
st.write(tickerDf)


# Bollinger bands
st.header('**Bollinger Bands**')

qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)




