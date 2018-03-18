# -*- coding: utf-8 -*-
"""
Created: Sun Mar 18 08:46:19 2018

@author: Shrutika Poyrekar

Modules:

Summary:
    
Location
"""


from __future__ import print_function
import json
from watson_developer_cloud import AssistantV1,DiscoveryV1
import sys
import requests



def connectToAssisstant(assistant_creds):
    assistant = AssistantV1(
    username=assistant_creds["username"],
    password=assistant_creds["password"],
    version='2017-04-21')
    return assistant

def connectToDiscovery(discoverNewsDreds):
    discoveryNews = DiscoveryV1(
    version='2017-08-01',
    username=discoverNewsDreds['username'],
    password=discoverNewsDreds['password'])
    return discoveryNews


def main():
    credentials = json.load(open('credentials.json'))
    companyNames= {"BOSCH": "BOSCHLTD.NS",
     "ICICI": "ICICIBANK.NS",
     "INFOSYS": "INFY.NS",
     "ITC": "ITC.NS",
     "JINDAL STEEL": "JINDALSTEL.NS"}
    url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=$$$$&apikey="
    url = url +credentials["api"]
    assistant=connectToAssisstant(credentials["assisstant"])
    discoveryNews=connectToDiscovery(credentials["discovery"])
    flag=True
    while(True):
        if flag:
            entry= "Bot: Welcome to Devil Wears prada:\n You can ask us any questions related to your portofolio, stock prices, companies\
            news and many more things.\nIf you want to leave type exit!!\n\nuser: "
            flag=False
        userInput = raw_input(entry)
        if userInput=="exit":
            print ("Good Bye")
            sys.exit(0)
        try:
            response = assistant.message(workspace_id=credentials["assisstant"]["workspace_id"],input={"text":userInput})
            text=str(response["output"]["text"][0])
            if "news" in text:
                #print(text)
                response=discoveryNews.query(environment_id="system",collection_id="news-en",query=userInput)
                sText=str(response["results"][0]["text"].encode("ascii","ignore"))
                sUrl=str(response["results"][0]["url"].encode("ascii","ignore"))
                sSentiment=response["results"][0]["enriched_text"]["sentiment"]["document"]
                text = "\nNews: "+sText+"\n\nFor more Info. visit: "+sUrl+"\n\nNews Sentiment: "+str(sSentiment["label"].encode("ascii","ignore"))+" Score: "+str(sSentiment["score"])
            elif "competitor" in text:
                response=discoveryNews.query(environment_id=credentials["discovery2"]["env_id"],collection_id=credentials["discovery2"]["collection_id"],query=userInput)
                text=str(response["results"][0]["text"].encode("ascii","ignore")).replace("no title\n\n","").strip()
            elif "stock" in text:
                #print (text)
                jText= json.loads(text)
                url1=url.replace("$$$$",companyNames[jText["company_name"]])
                r=json.loads(requests.get(url1).text)
                if len(str(jText["ask_date"])) >2:
                    text = jText["company_name"]+":\nOpen: "+r["Time Series (Daily)"][str(jText["ask_date"])]["1. open"]\
                                +"\nHigh: "+r["Time Series (Daily)"][jText["ask_date"]]["2. high"]\
                                +"\nLow: "+r["Time Series (Daily)"][jText["ask_date"]]["3. low"]\
                                +"\nClose: "+r["Time Series (Daily)"][jText["ask_date"]]["4. close"]
                else:
                    
                    text = jText["company_name"]+":\nOpen: "+r["Time Series (Daily)"]["2018-03-16"]["1. open"]\
                                +"\nHigh: "+r["Time Series (Daily)"]["2018-03-16"]["2. high"]\
                                +"\nLow: "+r["Time Series (Daily)"]["2018-03-16"]["3. low"]\
                                +"\nClose: "+r["Time Series (Daily)"]["2018-03-16"]["4. close"]
                
            
            entry = "Bot: "+text+"\n\nuser: "
        except Exception as e:
            print (e)
            sys.exit(0)
            entry = "Bot: Hey there this embarassing! I am having some issues. If anything urgernt call our toll free number 1800-1100-2200\n Or you can also ask me something else.\n\nuser: "