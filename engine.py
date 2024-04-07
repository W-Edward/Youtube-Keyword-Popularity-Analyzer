import pandas as pd
import numpy
import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from time import sleep
import json
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.linear_model import LinearRegression

#Note to self: Remember to edit the Geo param based on current location! 

keyword = sys.argv[1]

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
}

#Searching for Videos on Youtube (based on Youtube's Search Relevance Algorithm) using the given keyword 
#IMPORTANT: Videos obtained are only the ones uploaded in the past week
#Next, extracting the views of the videos and finding the mean views

meanViews = 0

#Videos that are only uploaded in the past week only
keyword_page = requests.get(f"https://www.youtube.com/results?search_query={keyword}&sp=EgIIAw%253D%253D", headers=HEADERS)
listOfViews = []
listOfDates = []

results = re.findall(r"\"title\":[^,]+,([^}]+)}", keyword_page.text)

for result in results:
    #per video
    info = re.findall(r"\"accessibility\":{\"accessibilityData\":{\"label\":(.*)$", result)
    if info:
        try:
            views, time = re.findall(r"by.+\s([a-z0-9,]+)\sviews?\s?(.*)", info[0], flags=re.IGNORECASE)[0]
            if (views == "No"):
                listOfViews.append("0")
            else:    
                listOfViews.append(views)
            #deducing upload time
            years = re.findall(r"([0-9]+)\syear", time)
            years = int(years[0]) if years else 0
            months = re.findall(r"([0-9]+)\smonth", time)
            months = int(months[0]) if months else 0
            weeks = re.findall(r"([0-9]+)\sweek", time)
            weeks = int(weeks[0]) if weeks else 0
            days = re.findall(r"([0-9]+)\sday", time)
            days = (int(days[0])+(years*365)+(months*30)) if days else (years*365)+(months*30)
            hours = re.findall(r"([0-9]+)\shour", time)
            hours = int(hours[0]) if hours else 0
            minutes = re.findall(r"([0-9]+)\sminute", time)
            minutes = int(minutes[0]) if minutes else 0
            seconds = re.findall(r"([0-9]+)\ssecond", time)
            seconds = int(seconds[0]) if seconds else 0

            listOfDates.append(datetime.today()-timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds))
        except:
            print(info) #skip videos where views are hidden

listOfViews = [int(re.sub(r",", "", view)) for view in listOfViews]
meanViews = np.mean(listOfViews)
minimumViews = np.min(listOfViews)
maximumViews = np.max(listOfViews)

listOfViews = np.array(listOfViews)
listOfDates = np.array(listOfDates)
listOfViews = listOfViews[np.argsort(listOfDates)]
listOfDates = np.sort(listOfDates)


'''
Currently not using Google Trends as the site detects bots very well
'''
#Using Google trends, we can actually check whether or not the keyword is trending. If linear regression line gradient 
#is increasing or high, then it is more trending. This should be 75% of what decides a keyword to be trending 


# from pytrends.request import TrendReq
# pytrends = TrendReq(hl='en-US', tz=420)
# pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='ID', gprop='youtube') #Trend on Youtube
# interest = pytrends.interest_over_time()

# #Plotting a Graph based on Google Trends Data
# interestData = interest.drop('isPartial', axis=1)

#Figure
fig, ax = plt.subplots(figsize=(8,4))
fig.patch.set_facecolor('white')

#Linear Regression to show the trend (The gradient m is what determines which word is trending)
df = pd.DataFrame({'time': listOfDates, 'count': listOfViews})
df.time = pd.to_datetime(df.time)

regr = LinearRegression()
regr.fit(df.time.values.reshape(-1, 1), df['count'].values.reshape(-1, 1))

# Make predictions using the testing set
y_pred = regr.predict(df.time.values.astype(float).reshape(-1, 1))
df['linreg'] = y_pred

#Plot
line1, = plt.plot(listOfDates, listOfViews, 'o', c='#86b9b0', markersize=5)
df.plot(x='time', y='linreg', color='#042630', alpha=0.75, ls='--', ax=ax)

#Labels and Axes
x_ticks = np.arange(min(listOfDates), max(listOfDates), timedelta(days=1))
plt.xlabel('Time')
plt.ylabel('Video Views')
plt.title(f'Popularity Trend of the Keyword "{keyword}"', loc='left', fontsize=10)
plt.grid(alpha=0.3, c="#d0d6d6")
ax.spines[['top', 'right']].set_visible(False)

plt.savefig(f"public/graphs/{keyword.lower()}.png")

peak = listOfDates[np.argmax(listOfViews)].strftime("%Y-%m-%d %X")

json_output = {"mean": f"{meanViews:.2f}", "peak": peak, "minimum": int(minimumViews), "maximum": int(maximumViews)} 
# json_output = {"mean": meanViews, "gradient": 1} 
print(json.dumps(json_output))

'''
Below is old code
'''

#Linear Regression to show the trend (The gradient m is what determines which word is trending)
# m, c = np.polyfit(np.arange(0, len(interestData.index)), interestData[keyword], 1)
# linReg = [(m*i+c) for i in np.arange(0, len(interestData.index))]

# line1, = plt.plot(interestData.index, keyword, data=interestData, c='#86b9b0')
# line2, = plt.plot(interestData.index, linReg)

#End Point Marker
# plt.plot(interestData.index[-1], interestData[keyword].iloc[-1], 'o', c='#86b9b0', markersize=10, alpha=0.3)
# plt.plot(interestData.index[-1], interestData[keyword].iloc[-1], 'o', c='#86b9b0', markersize=5)

# #Labels and Axes
# x_ticks = np.arange(min(interestData.index), max(interestData.index), timedelta(days=2))
# plt.ylim(0, 100)
# plt.xticks(x_ticks, fontsize=8)
# plt.yticks(fontsize = 8)
# plt.xlabel('Time')
# plt.ylabel('Interest')
# plt.title(f'Popularity Trend of the Keyword "{keyword}"', loc='left', fontsize=10)
# plt.grid(alpha=0.3, c="#d0d6d6")
# ax.spines[['top', 'bottom', 'right']].set_visible(False)

# #Linear Regression line
# plt.setp(line2, color='#042630', alpha=0.75, ls='--')

# #Annotations and Text
# plt.text(interestData.index[0], 20, f'$\\nabla$f (Gradient) = {m:.2f}', fontsize=7.5)
# plt.text(interestData.index[0], 15, f'f(0) = {c:.2f}', fontsize=7.5)

# plt.savefig(f"public/graphs/{keyword.lower()}.png")

# peak = interestData[keyword].idxmax().strftime("%Y-%m-%d %X")
# intercept = interestData[keyword].iloc[0]
# currentInterest = interestData[keyword].iloc[-1]

# json_output = {"mean": f"{meanViews:.2f}", "gradient": f"{m:.2f}", "peak": peak, "minimum": int(minimumViews), "maximum": int(maximumViews), 
#                "intercept": int(intercept), "currentInterest": int(currentInterest)} 
# # json_output = {"mean": meanViews, "gradient": 1} 
# print(json.dumps(json_output))









