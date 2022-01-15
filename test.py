#Get Market Fear Greed index
#Alireza, Jan 2022

from bs4 import BeautifulSoup
import requests

URL = "https://money.cnn.com/data/fear-and-greed/"
page = requests.get(URL)
# print(page.text)
soup = BeautifulSoup(page.content)
fear_greed_index = int(soup.find_all(id="needleChart")[0].find('li').get_text().split(':')[1].split('(')[0])
print(fear_greed_index)


###################################################################################################################
#get historical fead greed data for market from archive.org

dateitem = "20220106"
# url = f"https://web.archive.org/web/{dateitem}024917/https://money.cnn.com/data/fear-and-greed/"
url = f"https://web.archive.org/web/{dateitem}/https://money.cnn.com/data/fear-and-greed/"

page = requests.get(url)
# print(page.text)

soup = BeautifulSoup(page.content)
fear_greed_index = int(soup.find_all(id="needleChart")[0].find('li').get_text().split(':')[1].split('(')[0])
print(fear_greed_index)

###################################################################################################################
#get historical fear greed data for market from archive.org
#
#No cache !
h = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

import pandas as pd
import datetime

startdate = datetime.datetime(2021, 1, 1)
enddate = datetime.date.today()
# dt = pd.date_range(start=datetime.date.today(), periods=10, freq='B')
dt = pd.date_range(start=startdate , end = enddate, freq='B')

FEAR_GREED_DICT = {}
for dtitem in dt:
    dateitem = dtitem.strftime('%Y%m%d')
    print(dateitem)
    url = f"https://web.archive.org/web/{dateitem}/https://money.cnn.com/data/fear-and-greed/"
    pageget=False
    while not pageget:
        try:
            page = requests.get(url, headers=h)
            if page.status_code == 200:
                pageget=True
        except:
            pass
    soup = BeautifulSoup(page.content)
    fear_greed_index = int(soup.find_all(id="needleChart")[0].find('li').get_text().split(':')[1].split('(')[0])
    print(fear_greed_index)
    print(80*'=')
    FEAR_GREED_DICT[dtitem]  = fear_greed_index

df = pd.DataFrame.from_dict(FEAR_GREED_DICT, orient='index' , columns=['FEAR_GREED'] )
df.index = pd.to_datetime(df.index)


import yfinance as yf
Ticker='SPY'
yDF = yf.download(Ticker, start= startdate.strftime('%Y-%m-%d') , end = enddate.strftime('%Y-%m-%d'))

mergeDF=pd.merge(df , yDF ,  how='inner', left_index=True, right_index=True)
mergeDF.to_csv(f'{Ticker}.csv')


import matplotlib.pyplot as plt
plt.plot(mergeDF.Close)
plt.plot(mergeDF.FEAR_GREED)
plt.show()

ax = mergeDF.Close.plot()
ax2 =mergeDF.FEAR_GREED.plot(secondary_y=True)
# ax2.set_ylim(-20, 50)
fig = ax.get_figure()
plt.show()



####################################################################################

fig,ax = plt.subplots()

ax.plot(mergeDF.Close, color="green", marker="o")
ax.set_xlabel("Date",fontsize=14)
ax.set_ylabel("Close",color="green",fontsize=14)
fig = ax.get_figure()
ax.set_title(f'{Ticker} vs. Market FEAR GREED indexing (CNN Money)')
ax2=ax.twinx()
ax2.plot(mergeDF.FEAR_GREED,color="red",marker="o")
ax2.set_ylabel("FEAR_GREED",color="red",fontsize=14)
ax.grid(True)
ax2.grid(True)
plt.show()


####################################################################################
#Seaborn Correlation

import seaborn as sns

mergeDF.reset_index(inplace=True)
fig, ax = plt.subplots()
ax2 = ax.twinx()
sns.regplot(x=mergeDF.index, y="Close", data=mergeDF, order=2, ax=ax)
sns.regplot(x=mergeDF.index,y="FEAR_GREED", data=mergeDF, order=2, ax=ax2)


ax2.legend(handles=[a.lines[0] for a in [ax,ax2]], labels=["Close", "FEAR_GREED"])
plt.show()

