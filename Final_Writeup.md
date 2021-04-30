# Reddit/wallstreetbets submission analysis

---

Brian Nam

## Abstract

---

The goal of this project is to obtain a large dataset through a pipeline and deploy the data through a webapp. Reddit subgroup wallstreetbets became a big issue during January and February due to the Gamestop short squeeze by the hedge funds. Reddit submission data was gathered through their api to find correlation or interesting contact points between the subreddit and certain stocks. 

## Design

---

By constructing a pipeline through multiple functions we were able to update the MYSQL database and streamlit in matter of minutes.
Use PRAW to update the MYSQL database, Jupyternotebook to process the new data to fit the MYSQL database for streamlit then inserted, Streamlit is redeployed with the updated data.

## Data

---

The dataset contains 882,928 submissions from 1/1/21 to 4/28/20 with 5 variables each(Author, score, selftext, time, title, url).

## Algorithms

---

Spacey was used to pull out stock mentions from submission titles. Then the mentions were aggregated to plot graphs.  


## Tools

---

* Reddit api, PRAW, pushshift.io for data acquisition
* Pandas, numpy, sql, spacey for data manipulation
* Seaborn, matplotlib, Streamlit for data visualization

## Communication

---

* Slides were made for the presentation to give a better understanding of the analysis and pipe line.
* Streamlit was used to deploy a web app for interative graphs.