#!/usr/local/bin/python
# -- coding: utf-8 --

##### ------ Open Delays Program v1.2------ #####

import MySQLdb #for db access
import urllib #for internet access
import time #to calculate current date and hour

class Database:

    host = 'localhost'
    user = 'root'
    password = ''
    db = 'OpenDelays'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def __del__(self):
        self.connection.close()

def pdidb(l_Data,nbf,stime): #put data in database
    db = Database() #init class database and attributes
    for m in range (0,nbf):
        query1 = """
            INSERT INTO opendelays_uk
            (`date`, `current_station`, `plan_time_arr`, `real_time_arr`, `from_station`, `pl`, `id_train`, `toc`, `to_station`, `plan_time_dep`, `real_time_dep`)
            VALUES"""
        query2="('"+l_Data[0][m]+"','"+l_Data[10][m]+"','"+l_Data[1][m]+"','"+l_Data[2][m]+"','"+l_Data[3][m]+"','"+l_Data[4][m]+"','"+l_Data[5][m]+"','"+l_Data[6][m]+"','"+l_Data[7][m]+"','"+l_Data[8][m]+"','"+l_Data[9][m]+"')"
        query=query1+query2
	if len(l_Data[6][m]) > 1:
            if len(l_Data[1][m]) > 3:
                h=l_Data[1][m]
                if h[0]+h[1] == stime[:2]:db.insert(query)
            else : db.insert(query)

def no_none(l_Data,nbf):
    for m in range (0,nbf):
        for n in range (0,11):
            if l_Data[n][m] is None: l_Data[n][m]=""
            h=l_Data[n][m]
            if (n==1 or n==2 or n==8 or n==9) and len(h)> 3 and h != "pass" and h != "Canc"  and h[2]!=":":
                h=h[0]+h[1]+":"+h[2]+h[3]
                l_Data[n][m]=h
    return l_Data
    
def openUrl(station,date,time):
    #open website page
    #http://www.realtimetrains.co.uk/search/advanced/ABW/2014/10/31/1200
    u = "http://www.realtimetrains.co.uk/search/advanced/"+station+'/'+date+'/'+time
    website= urllib.urlopen(u).read()
    return website

def getStations():
    l_stations=[];station=""
    f=open("project/stations_uk.txt","r")
    stationsF=f.read()
    stationsF=stationsF.replace("\n","")
    sizef=len(stationsF)
    for i in range (0,sizef):
        station=station+stationsF[i]
        if len(station) == 3:l_stations.append(station); station=""
    return l_stations

def getStation(data):
    station=""
    station=search(data,"<title>","</title>",0)
    station=search(station,"from ","<",0)
    return station

def getData(l_stations):
    l_data=[[],[],[],[],[],[],[],[],[],[],[],[]];nb_res=0; nb_commit=0;
    localtime = time.localtime(time.time())
    stime = str(localtime.tm_hour-2)
    if int(stime) < 10: stime="0"+str(stime)+"10"
    else:stime=stime+"10"
    day=int(time.strftime("%d"))-1
    if str(localtime.tm_hour)=="00":sdate=time.strftime("%y/")+time.strftime("%m/")+str(day);
    else: sdate=time.strftime("20%y/%m/%d")
    dbdate=time.strftime("%y-%m-%d")
    for i in range (0,len(l_stations)):
        data=openUrl(l_stations[i],sdate,stime);
        #print str(i)+" / "+str(len(l_stations))
        if len(data) > 100:
            data2=search(data,"/thead","footer",0)
            nb_res = count(data,'<tr')
	    nb_commit = nb_commit + nb_res
            for j in range (0, nb_res):
                data3=search(data2,"<tr","</tr>",j)
                for k in range (1,10):
                    data4=search(data3,"<td","</td>",k)
                    if k == 3 or k == 7 or k == 5: rec = 1
                    else: rec = 0
                    data5=search(data4,chr(62),chr(60),rec)
                    #print data5
                    l_data[k].append(data5)
                l_data[10].append(getStation(data))
                l_data[0].append(dbdate)
    no_none(l_data,nb_commit)
    pdidb(l_data,nb_commit,stime)
                
def count(data, word):
    tmpData=''; nb=0
    for i in range (0, len(data)):
        tmpData=tmpData+data[i]
        if tmpData[-len(word):]== word:nb=nb+1; tmpData=""
        if i == len(data)-1: return nb
            
def search(data, word1, word2,nb):
    tmpData='';tmpData2=''; l_db=[[],[]];start=0;data=str(data)
    for i in range (0, len(data)):
        tmpData=tmpData+data[i]
        if start == 1: tmpData2=tmpData2+data[i]
        if tmpData[-len(word1):]== word1:i=i+1;start=1;
        if tmpData[-len(word2):]== word2:
            if nb != 0: nb=nb-1; start=0; tmpData2=''
            else: return tmpData2[:-1];
        
def pTime():
    localtime = time.localtime(time.time())
    t = str(localtime.tm_hour)+":"+str(localtime.tm_min)+":"+str(localtime.tm_sec)
    return t


t1= pTime()
l_stations=getStations()
getData(l_stations)
t2= pTime()
print t1+"   "+t2
