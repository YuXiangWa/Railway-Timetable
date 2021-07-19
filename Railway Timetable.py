# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 15:39:58 2021

@author: user
"""
# [https://tip.railway.gov.tw/tra-tip-web/tip](https://tip.railway.gov.tw/tra-tip-web/tip)


import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
url = 'https://tip.railway.gov.tw/tra-tip-web/tip'
staDic = {} #字典:儲存火車站名稱與代碼
today = time.strftime('%Y/%m/%d')
sTime = '06:00'
eTime = '12:00'
Timetable = []
def getTrip():
    resp = requests.get(url)
    if resp.status_code != 200:
        print('URL發生錯誤：' + url)
        return
    
    soup = BeautifulSoup(resp.text, 'html5lib')
    stations = soup.find(id = 'cityHot').ul.find_all('li')
    for station in stations: #取得車站名稱與代碼
        stationName = station.button.text
        stationId = station.button['title']
        staDic[stationName] = stationId #站名(key): 代碼-站名(value)。 ex:臺南 4220-臺南
    
    csrf = soup.find(id = 'queryForm').find('input',{'name':'_csrf'})['value']
    formData = {
        'trainTypeList':'ALL',
        'transfer':'ONE',
        'startOrEndTime':'true',
        'startStation':staDic['臺南'],
        'endStation':staDic['臺中'],
        'rideDate':today,
        'startTime':sTime,
        'endTime':eTime, 
        '_csrf':csrf
    }
    
    queryUrl = soup.find(id='queryForm')['action'] #準備表單資訊
    qResp = requests.post('https://tip.railway.gov.tw'+queryUrl, data=formData) #表單查詢車次網址，第二個參數為表單資訊
    qSoup = BeautifulSoup(qResp.text, 'html5lib')
    trs = qSoup.find_all('tr', 'trip-column') #回傳車次資料(列)
    
    for tr in trs:
        td = tr.find_all('td') #使td標籤將資料一欄欄區隔
        Timetable.append((td[0].ul.li.a.text, td[1].text, td[2].text)) #車種車次、出發時間、抵達時間
        
getTrip()
Timetable = pd.DataFrame(Timetable,columns=['車種車次','出發時間','抵達時間'])