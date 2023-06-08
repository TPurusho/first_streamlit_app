# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 11:53:02 2023

@author: TharunKumarPurushoth
"""

import yfinance as yf
import streamlit as st
import json
import pandas as pd
import time


#import pandas as pd
st.set_page_config(layout="wide")
st.write("""
         # Simple Stock Market Graph""")

# Specify the ticker symbol for the stock
st.write(""" ### Which stock you want to see? Please enter below""")
tickerSymbolName= st.text_input('Enter the tickerSymbol here', value='')
if st.button("Enter"):
    tickerSymbol = tickerSymbolName
    
    # Get data from the ticker
    tickerData = yf.Ticker(tickerSymbol)
    
    time.sleep(1)
    st.subheader('Company details') 
    company = tickerData.info
    
    # Convert JSON data to DataFrame
    df = pd.DataFrame([company])
    st.write(df)

    tickerDf = tickerData.history(period='1y', start='2000-5-31', end='2023-06-07')

    # Display line charts for each column
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Close Chart')
        st.line_chart(tickerDf.Close)
    with col2:
        st.subheader('Volume Chart')
        st.line_chart(tickerDf.Volume)
    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Open Chart')
        st.line_chart(tickerDf.Open)
    with col4:
        st.subheader('High Chart')
        st.line_chart(tickerDf.High)
    
    #financials
    #st.subheader('Company Financials')
    #financials = tickerData.financials
    #quarterly_financials = tickerData.quarterly_financials
    #balance_sheet = tickerData.balance_sheet
    #cashflow = tickerData.cashflow
    
    #st.write(financials)
    #st.write(quarterly_financials)
    #st.write(balance_sheet)
    #st.write(cashflow)
    
    #option data
    optionsData = tickerData.option_chain()
    
    #convert yfinance options into dataframe
    optionsData = pd.DataFrame(optionsData.calls)
    st.write(optionsData)
    

