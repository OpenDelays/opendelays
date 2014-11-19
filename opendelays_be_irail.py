#!/usr/local/bin/python
# -- coding: utf-8 --

##### ------ Open Delays Program v1.2------ #####

import MySQLdb #for db access
import urllib #for internet access
import time #to calculate current date and hour

class Database:

    host = 'localhost'
    user = 'root'
    password = 'wemove_odnsom1ra'
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
        
def pdidb(l_Data,nbf): #put data in database
    db = Database() #init class database and attributes
    for m in range (0,nbf):
        query1 = """
            INSERT INTO opendelays_be
            (`datetime`, `arrivalStation`, `delay`, `type-num`)
            VALUES"""
        query2="('"+l_Data[0][m]+"','"+l_Data[1][m]+"','"+l_Data[2][m]+"','"+l_Data[3][m]+"')"
        query=query1+query2
        db.insert(query)

def openUrl(station,date,time):
    #open website page
    u1 = 'http://api.irail.be/liveboard/?station='+station
    u2 = '&fast=true&date='+date
    u3 = '&time='+time+'&arrdep=arr'
    u=u1+u2+u3
    try: 
        website= urllib.urlopen(u).read()
        if website is not None: return website
        else:return ''
    except:openUrl(station,date,time)

def getStations():
    l_stations=[]
    nbCh=0
    url="http://api.irail.be/stations/"
    stationsF=urllib.urlopen(url).read()
    sizef=len(stationsF)
    station=""
    for i in range (0,sizef):
        if stationsF[i] == chr(62) or stationsF[i] == chr(60):
            nbCh=nbCh+1
            if len(station) > 3:
                for j in range (0,len(station)/2):
                    if station[j]=="/":station=station[j+1:]
                l_stations.append(station)
            station=''
        if (nbCh % 2 == 0) and (nbCh > 2) and (stationsF[i] != chr(62)):
            station=station+stationsF[i]
    return l_stations

def getData(l_stations):
    l_data=[[],[],[],[]]; nb=0
    localtime = time.localtime(time.time())
    stime = str(localtime.tm_hour-1)+"00"
    if len(stime)==3:stime="0"+stime
    dbtime = str(localtime.tm_hour-1)+":00"
    day=int(time.strftime("%d"))-1
    if str(localtime.tm_hour-1)=="23":sdate=time.strftime("%m")+str(day)+time.strftime("%y")
    else: sdate=time.strftime("%m%d%y")
    for i in range (0,len(l_stations)):
        data=openUrl(l_stations[i],sdate,stime); buff=0
        #print str(i)+" / "+str(len(l_stations))
        while data is not None and buff < len (data)-90 and len(data)>270:
            dbdate=search(data, 'time formatted="',buff)[1][-1]
            dbdate=dbdate.replace("T"," ");dbdate=dbdate.replace("Z","");
            if len(dbdate) > 15 :
                if (dbdate[-8]+dbdate[-7])== stime[0]+stime[1]:
                    l_data[0].append(dbdate)
                    l_data[1].append(l_stations[i])
                    l_data[2].append(search(data, 'delay="',buff)[1][-1])
                    l_data[3].append(search(data, '<vehicle>BE.NMBS.',buff)[1][-1])
                    buff=(search(data, '<vehicle>BE.NMBS.',buff)[0][-1])
                    nb=nb+1
                    #print nb
                else :buff = (search(data, '<vehicle>BE.NMBS.',buff)[0][-1])
            else:buff=len(data)
    pdidb(l_data,nb)

def search(data, word, buff):
    tmpData=''; j=0; l_db=[[],[]]
    for i in range (buff, len(data)):
        tmpData=tmpData+data[i]
        if tmpData[-len(word):]== word:
            i=i+1; tmpData=''
            while data[i+j] != chr(34) and data[i+j] != chr(60): tmpData=tmpData+data[i+j]; j=j+1;
            l_db[0].append(i+j); l_db[1].append(tmpData);
            return l_db
    l_db[0].append(i+j); l_db[1].append('');
    return l_db
        
def pTime():
    localtime = time.localtime(time.time())
    t = str(localtime.tm_hour)+":"+str(localtime.tm_min)+":"+str(localtime.tm_sec)
    return t

t1= pTime()

l_stations=getStations()
getData(l_stations)

t2= pTime()
print t1+"   "+t2

##http://api.irail.be/vehicle/?id=BE.NMBS.IC2340&fast=true
