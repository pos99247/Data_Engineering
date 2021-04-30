import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

connection = pymysql.connect(host='localhost', user='root', password='pos99247', db='mydb', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

option = st.sidebar.selectbox("Dashboard?", ('wallstreetbets', 'chart', 'pattern'))

if option ==  'wallstreetbets':
    st.subheader('wallstreetbets')

    cursor.execute('''SELECT * FROM daybyday''')
    table2_rows = cursor.fetchall()
    daybyday = pd.DataFrame(table2_rows)
    days = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '1-7', '1-8', '1-9', '1-10', '1-11', '1-12', '1-13', '1-14', '1-15'
            , '1-16', '1-17', '1-18', '1-19', '1-20', '1-21', '1-22', '1-23', '1-24', '1-25', '1-26', '1-27', '1-28'
            , '1-29', '1-30', '1-31', '2-1', '2-2', '2-3', '2-4', '2-7', '2-8', '2-9', '2-10', '2-11', '2-12'
            , '2-13', '2-14', '2-15', '2-16', '2-17', '2-18', '2-19', '2-20', '2-21', '2-22', '2-23', '2-24', '2-25'
            , '2-26', '2-27', '3-2', '3-3', '3-4', '3-5', '3-7', '3-8', '3-9', '3-10', '3-11', '3-12',
            '3-13', '3-14', '3-15', '3-16', '3-17', '3-27', '3-28', '3-29', '3-30', '3-31',
            '4-1', '4-2', '4-3', '4-4', '4-5', '4-6', '4-7', '4-8', '4-9', '4-13', '4-14',
            '4-15', '4-16', '4-17', '4-18', '4-19', '4-20', '4-21', '4-22', '4-23', '4-24', '4-25', '4-26']

    sns.barplot(x='full_date', y='title', data=daybyday)
    plt.xticks(np.arange(0, 99, step=28), ['Jan', 'Feb', 'Mar', 'Apr'])
    plt.xlabel("From 1/1 to 4/26")
    plt.ylabel("Submissions")
    plt.title("Daily reddit submissions from 1/1 to 4/26")
    show_graph = st.checkbox('Show Graph', value=True)
    if show_graph:
        st.pyplot()
    # Import table DF from MYSQL DB
    cursor.execute('''SELECT * FROM test4''')
    table_rows = cursor.fetchall()
    test = pd.DataFrame(table_rows)

    # Date slider
    date_input = st.slider('Date Filter', test['date_only'].min(), test['date_only'].max())

    # Function that takes date as a string and outputs the graph
    def daily_mention_grapher1(date):
        index = list(test[test['date_only'] == pd.to_datetime(date)].index)[0]
        row = test[['GME', 'AMC', 'NOK', 'NAKD', 'PLTR', 'BB', 'SLV', 'RH', 'APHA', 'AMD', 'AAC',
                     'CCIV', 'HODL', 'BBBY', 'ZOM', 'APPLE', 'SOS', 'KOSS', 'AMAZON']].loc[index]
        row = row[row > 0]
        row = row.sort_values()
        row.plot(kind='barh')
        plt.title('mentions of stocks on wallstreetbets')
        st.dataframe(row)
        st.pyplot()


    daily_mention_grapher1(str(date_input))
