import snowflake.connector
import streamlit as st
import pandas as pd
import plotly.express as px

account = 'px57479.central-india.azure'
username = 'sushmtha'
password = 'Jamuna@31'
role = 'ACCOUNTADMIN'
warehouse = 'COMPUTE_WH'
database = 'SNOWFLAKE_SAMPLE_DATA'
schema = 'TPCH_SF1'
table = 'ORDERS'

conn = snowflake.connector.connect(user=username, password=password, account=account, warehouse=warehouse,
                                   schema=schema, database=database, role=role)

# Load sample data
table = pd.read_sql(f'select * from {database}.{schema}.{table} limit 100', conn)
table1 = pd.DataFrame(table)
st.write(table1)

column_names = table1.columns.tolist()

# Input widgets to modify x_column and y_column
x_column = st.selectbox("X-Axis Column", options=column_names)
y_column = st.selectbox("Y-Axis Column", options=column_names)

# Create a new dataframe with selected columns
if x_column and y_column:
    selected_data = table1[[x_column, y_column]]
    st.subheader("Selected Data")
    st.dataframe(selected_data)  # Display the selected data in a DataFrame widget

# User inputs to modify specific cells
cell_row = st.number_input("Row number to edit", min_value=0, max_value=len(selected_data)-1, value=0, step=1)
cell_column = st.selectbox("Column to edit", options=selected_data.columns)
cell_value = st.text_input("New cell value", value=selected_data.loc[cell_row, cell_column])

# Update the selected_data DataFrame with user inputs
if st.button("Update Cell"):
    selected_data_copy = selected_data.copy()  # Create a copy of the selected_data dataframe
    selected_data_copy.loc[cell_row, cell_column] = cell_value
    st.success("Cell value updated!")
    st.write(selected_data_copy)
# Create two columns for dashboard layout
col1, col2 = st.columns(2)

# Graph 1: Bar Chart (Plotly)
with col1:
    st.subheader('Bar Chart (Plotly)')
    bar_chart_data = selected_data_copy.groupby(x_column)[y_column].sum().reset_index()
    fig_bar = px.bar(bar_chart_data, x=x_column, y=y_column)
    st.plotly_chart(fig_bar)

# Graph 2: Line Chart (Plotly)
with col2:
    st.subheader('Line Chart (Plotly)')
    line_chart_data = selected_data_copy.groupby(x_column)[y_column].sum().reset_index()
    fig_line = px.line(line_chart_data, x=x_column, y=y_column)
    st.plotly_chart(fig_line)

# Graph 3: Scatter Plot (Plotly)
col3, col4 = st.columns(2)

with col3:
    st.subheader("Scatter Plot (Plotly)")
    scatter_data = selected_data_copy
