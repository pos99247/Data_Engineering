import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import spacy
from spacy import displacy
from sqlalchemy import create_engine
from datetime import date
from datetime import datetime
import datetime
from psaw import PushshiftAPI

# start time should be the last fulldate in the DF prior to update
# end time shoudl be the present date at the time of the update
def starttime():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='pos99247',
                                 db='mydb')
    cursor = connection.cursor()
    cursor.execute('''SELECT time FROM wallstreetbets ORDER BY time DESC LIMIT 1''')
    time = cursor.fetchall()
    year = int(time[0]['time'][:4])
    month = int(time[0]['time'][5:7])
    day = int(time[0]['time'][8:10])
    return datechanger(year, month, day)

def endtime():
    today = date.today()
    d1 = today.strftime("%Y/%m/%d")
    year = int(d1[:4])
    month = int(d1[5:7])
    day = int(d1[8:10])
    return datechanger(year, month, day)

# reddit data function takes in a specific form of date
def datechanger(year, month, day):
    time = int(datetime.datetime(year, month, day).timestamp())
    return time

# input the time frame then wallstreetbets is updated with the new submissions
def get_reddit_data(starttime, endtime):
    api = PushshiftAPI()
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='pos99247',
                                 db='mydb')
    cursor = connection.cursor()

    submissions = api.search_submissions(after=starttime,
                                         before=endtime,
                                         subreddit='wallstreetbets',
                                         filter=['url', 'author', 'title', 'subreddit', 'score', 'selftext',
                                                 'created_utc'])

    for submission in submissions:
        submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()
        try:
            cursor.execute("""
            INSERT INTO wallstreetbets (time, author, title, score, selftext, url)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
            submitted_time, submission.author, submission.title, submission.score, submission.selftext, submission.url))

            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()

# Pull the updated rows as DataFrame
def updated_rows():
    connection = pymysql.connect(host = 'localhost',
                            user= 'root',
                            password = 'pos99247',
                            db = 'mydb',
                            cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()


    cursor.execute("""SELECT author, time FROM wallstreetbets WHERE time > date_sub(now(), interval 1 week)""")
    rows = cursor.fetchall()
    update = pd.DataFrame(rows)
    return update

# Uses nlp to distinguish which words are significant in the title column
def getmention(text):
    nlp = spacy.load('en_core_web_sm')
    doc=nlp(text)
    org_list = []
    for entity in doc.ents:
        if entity.label_ == 'ORG':
            org_list.append(entity.text)
    org_list = list(set(org_list))
    return org_list

# Stock class is made to make the converting process easier
class Stock:
    def __init__(self, name):
        self.name = name

    # Check stock from ORG column
    def check(self, list):
        if self.name in list:
            return 1
        else:
            return 0

# Important stock listing that we will look into.
GME = Stock('GME')
AMC = Stock('AMC')
NOK = Stock('NOK')
NAKD = Stock('NAKED')
PLTR = Stock('PLTR')
BB = Stock('BB')
SLV = Stock('SLV')
RH = Stock('RH')
APHA = Stock('APHA')
AMD = Stock('AMD')
AAC = Stock('AAC')
CCIV = Stock('CCIV')
HODL = Stock('HODL')
BBBY = Stock('BBBY')
ZOM = Stock('ZOM')
APPLE = Stock('APPLE')
SOS = Stock('SOS')
KOSS = Stock('KOSS')
AMAZON = Stock('Amazon')
stock_list = [GME, AMC, NOK, NAKD, PLTR, BB, SLV, RH, APHA, AMD, AAC, CCIV, HODL, BBBY, ZOM, APPLE, SOS, KOSS, AMAZON]

# updated rows are then processed to fit back into the sql server
def dataprocessing(df):
    stock_list = [GME, AMC, NOK, NAKD, PLTR, BB, SLV, RH, APHA, AMD, AAC, CCIV, HODL, BBBY, ZOM, APPLE, SOS, KOSS, AMAZON]
    stock_column_list = ['GME', 'AMC', 'NOK', 'NAKD', 'PLTR', 'BB', 'SLV', 'RH', 'APHA', 'AMD', 'AAC',
                     'CCIV', 'HODL', 'BBBY', 'ZOM', 'APPLE', 'SOS', 'KOSS', 'AMAZON']
    df['time'] = pd.to_datetime(df['time'])
    df['day'] = df['time'].dt.day
    df['month'] = df['time'].dt.month
    df['year'] = df['time'].dt.year
    df['full_date']= pd.to_datetime(df[['year','month','day']])
    df = df.sort_values('time', ascending=True)
    df['org'] = df['title'].apply(getmention)
    for stock in stock_list:
        df[stock.name] = df['org'].apply(stock.check)
    test = df.groupby(['full_date']).agg({'GME':'sum', 'AMC':'sum', 'NOK':'sum', 'NAKD':'sum', 'PLTR':'sum',
                                           'BB':'sum', 'SLV':'sum', 'RH':'sum', 'APHA':'sum',
                                           'AMD':'sum', 'AAC':'sum','CCIV':'sum', 'HODL':'sum', 'BBBY':'sum',
                                           'ZOM':'sum', 'APPLE':'sum', 'SOS':'sum', 'KOSS':'sum', 'AMAZON':'sum'})
    for column in stock_column_list:
        column_cumsum = column + "_sum"
        test[column_cumsum] = test[column].cumsum()
    test[['full_date']] = test.index
    test['date_only'] = test['full_date'].dt.date
    del test['full_date']
    return test

# Processed dataframe is inserted back into the database to update the changes in streamlit graph
def update_graph(df):
    hostname="localhost"
    dbname="mydb"
    uname="root"
    pwd="pos99247"
    engine = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'.format(host=hostname, db=dbname, user=uname, pw=pwd))
    df.to_sql('test4', engine, if_exists = 'append')