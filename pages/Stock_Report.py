import streamlit as st
from Home import tickerData,start,end
from streamlit_pandas_profiling import st_profile_report 
from pandas_profiling import profile_report

# get the historical prices for this ticke
tickerDf = tickerData.history(period='1d', start=start, end=end)
tickerDf.reset_index(inplace=True)
profiling = tickerDf.profile_report()

st_profile_report(profiling)