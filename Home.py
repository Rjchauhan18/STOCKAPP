import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime , date,timedelta
import cufflinks as cf
# import matplotlib.pyplot as plt
# import plotly
import plotly.graph_objects as go
# import pandas_profiling
# from prophet import Prophet
from patterns import Company_Name

# import smtplib as smt 

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









with st.sidebar:
    st.sidebar.markdown(' # Stock Price Analysis ')
    st.sidebar.title(f"Welcome ")

    
    # get current datetime
    dt = datetime.now()
        
    DAY = dt.strftime('%A')
   
    if DAY == 'Saturday' or DAY == 'Sunday':
        start_date =  date.today() - timedelta(days=3)
        end_date = date.today() - timedelta(days=2)
    else:
        start_date = date.today()
        end_date = date.today() + timedelta(days=1)


    start= st.sidebar.date_input("start date", start_date)
    end = st.sidebar.date_input("End date", end_date) 

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

   



def app():


    # get the historical prices for this ticke
    tickerDf = tickerData.history(period=periods,interval=timeframes, start=start, end=end)
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
        @st.cache_data
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
  
    
  
if __name__== '__main__':
    app()

    
