import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hot-boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avacado Toast')
streamlit.markdown('Market')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
#reading a CSV file from the aws bucket by using a pandas
fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
# set a Fruit column as index
fruit_list = fruit_list.set_index('Fruit')

# here I put pick list so they can pick the fruit they want
fruit_selected = streamlit.multiselect("Pick Some Fruits:",list(fruit_list.index),['Avocado','Strawberries'])

fruit_to_show = fruit_list.loc[fruit_selected]

streamlit.dataframe(fruit_to_show)
