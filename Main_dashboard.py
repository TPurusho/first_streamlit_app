# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:44:25 2023

@author: TharunKumarPurushoth
"""

import snowflake.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sidebar = st.sidebar

with sidebar:
    st.markdown(':snowflake: Snowflake Connection')
    account = st.text_input("Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.text_input("Role")
    warehouse = st.text_input("Warehouse")
    database = st.text_input("Database")
    schema = st.text_input("Schema")
    table = st.text_input("Table")
    connect = st.button("Connect to Snowflake")

conn = None  # Initialize connection variable
table1 = None
x_column = None
y_column = None
plot_button = None
selected_data = None

# Connect to Snowflake on button click
if connect:
    if not username:
        st.warning("Please enter a username.")
try:
    conn = snowflake.connector.connect(user=username, password=password, account=account, warehouse=warehouse,
                                       schema=schema, database=database, role=role)
    st.header(f'Snowflake Table : {table}')

    table = pd.read_sql(f'select * from {database}.{schema}.{table} limit 100', conn)
    table1 = pd.DataFrame(table)
    st.write(table1)

    st.subheader('Graph')
    # Select x-axis and y-axis columns
    column_names = table1.columns.tolist()
    x_column = st.selectbox("X-Axis Column", options=column_names)
    y_column = st.selectbox("Y-Axis Column", options=column_names)

 
    # Create a new dataframe with selected columns
    if x_column and y_column:
        selected_data = table1[[x_column, y_column]]
        st.subheader("Selected Data")
        st.write(selected_data)
           

    def show_bar_chart():
        st.subheader('Bar Chart')
        bar_chart_data = table1.groupby(x_column)[y_column].sum()
        plt.figure(figsize=(8, 6))
        plt.bar(bar_chart_data.index, bar_chart_data.values)
        plt.xlabel('Category')
        plt.ylabel('Sales')
        plt.title('Total Sales by Category')
        plt.xticks(rotation=45)
        st.pyplot(plt)
    
    def show_line_chart():
        st.subheader('Line Chart')
        line_chart_data = table1.groupby(x_column)[y_column].sum()
        plt.figure(figsize=(8, 6))
        plt.plot(line_chart_data.index, line_chart_data.values)
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        #plt.title('Total Profit by Year')
        plt.xticks(rotation=45)
        st.pyplot(plt)
    
    def show_scatter_plot():
        st.subheader('Scatter Plot')
        scatter_plot_data = table1.sample(100)  # Randomly sample 100 data points
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=scatter_plot_data, x=x_column, y=y_column)
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        #plt.title('Sales vs Profit')
        st.pyplot(plt)
    
    # Main dashboard layout
    st.title('Dashboard')
    
    # Chart selection
    chart_options = ['Bar Chart', 'Line Chart', 'Scatter Plot']
    selected_chart = st.selectbox('Select a chart', chart_options)
    plot_button = st.button("Plot")
    st.text("If you want to see all the chart kindly click Plot_All button")
    plot_all_button = st.button("Plot_All")
    # Display selected chart
    if selected_chart == 'Bar Chart' and plot_button:
        show_bar_chart()
    elif selected_chart == 'Line Chart' and plot_button:
        show_line_chart()
    elif selected_chart == 'Scatter Plot' and plot_button:
        show_scatter_plot()
    elif plot_all_button:
        col1, col2 = st.columns(2)
        with col1:
            show_bar_chart()
        with col2:
            show_line_chart()
        #with st.columns():
        show_scatter_plot()

except snowflake.connector.errors.Error as e:
    st.error(f"Connection error: {str(e)}")
























