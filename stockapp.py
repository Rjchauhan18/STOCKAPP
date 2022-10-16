import yfinance as yf
import pandas as pd
import streamlit as st
import datetime as dt
#import cufflinks as cf
import matplotlib.pyplot as plt


#app title
st.markdown(
    """
    Stock Price App\n
    Shown are the stock price data for the query companys!

    """
)

st.write('---')

#sidebar
st.sidebar.subheader('Query parameter')
start_date = st.sidebar.date_input("start date", dt.date(2021,1,1))
End_date = st.sidebar.date_input("End date", dt.date(2022,1,1))

# Retrieving tickers data
ticker_list = pd.read_csv('https://github.dev/Rjchauhan18/STOCKAPP/blob/f8538a2231f201e992aba423105e2c70fe7f4c56/NIFTYSTOCK.txt')

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
"""
qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)
"""



