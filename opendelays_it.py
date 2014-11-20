#!/usr/local/bin/python
# -- coding: utf-8 --

##### ------ Open Delays IT v1.0------ #####

import MySQLdb #for db access
import urllib #for internet access
import time #to calculate current date and hour
from time import gmtime, strftime
import datetime

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

def pdidb(l_Data,nbf): #put data in database
    db = Database() #init class database and attributes
    #print 'enregistrement en cours  '+str(nbf)
    for m in range (0,nbf):
        query1 = """
            INSERT INTO opendelays_it
            (`from_station`, `plan_time_arr`, `delay`, `current_station`, `id_train`, `to_station`)
            VALUES"""
        query2="('"+l_Data[0][m]+"','"+l_Data[2][m]+"','"+str(l_Data[3][m])+"','"+l_Data[1][m]+"','"+str(l_Data[4][m])+"','"+l_Data[5][m]+"')"
        query=query1+query2
        if int(l_Data[3][m]) > -1000 and int(l_Data[3][m]) < 1000 :db.insert(query)

def wordList():
    word_list=[]
    word_list.append('"stazione"')#FROM
    word_list.append('"stazione"')#Current
    word_list.append('"programmata"')#arrivé prévu  format datetime
    word_list.append('"effettiva"')#arrivé effective
    word_list.append('"stazione"')#TO
    return word_list
    
def openUrl(station):
    #open website page
    #http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/tratteCanvas/N00001/13
    u = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/tratteCanvas/"+station
    website= urllib.urlopen(u).read()
    #print u
    return website

def getStations():
    l_stations=[];station="";
    f=open("project/stations_it.txt","r")
    stationsF=f.read()
    stationsF=stationsF.replace("\n","")
    sizef=len(stationsF)
    for i in range (0,sizef):
        if stationsF[i-1]==chr(124):
            while stationsF[i]!=chr(45):
                station=station+stationsF[i]
                i=i+1
            id_train.append(int(station))
            station=stationsF[i+1]+stationsF[i+2]+stationsF[i+3]+stationsF[i+4]+stationsF[i+5]+stationsF[i+6]+"/"+station
            l_stations.append(station)
            station=''
    return l_stations

def getData(l_stations):
    l_data=[[],[],[],[],[],[]];nb_res=0;dbdate=1;word_list=wordList();ts=0; nb_t=0
    for i in range (0,len(l_stations)):
        data=openUrl(l_stations[i]);
        #print str(i)+" / "+str(len(l_stations))
        nb_res=count(data,word_list[2])
        if nb_res != 0:
            if search(data,word_list[2],nb_res-1)!='null':
                if verifTimeStamp(int(search(data,word_list[2],nb_res-1)))== 1 :
                    for j in range (0,nb_res):
                        if search(data,word_list[2],j)!='null' and search(data,word_list[3],j)!='null':
                            nb_t=nb_t+1
                            l_data[0].append(search(data,word_list[0],0))
                            l_data[1].append(search(data,word_list[0],j*2))
                            l_data[2].append(timeStampToDate(int(search(data,word_list[2],j))))
                            ts =search(data,word_list[3],j)
                            l_data[3].append(timeStampToDelay(int(search(data,word_list[2],j)),int(ts)))
                            l_data[4].append(id_train[i])
                            l_data[5].append(search(data,word_list[0],count(data,word_list[0])-1))
    pdidb(l_data,nb_t)

def count(data, word):
    tmpData=''; nb=0
    if len(data)==0:return 0
    for i in range (0, len(data)):
        tmpData=tmpData+data[i]
        if tmpData[-len(word):]== word:nb=nb+1; tmpData=""
        if i == len(data)-1: return nb
            
def search(data, word, nb):
    tmpData='';tmpData2=''; l_db=[[],[]];start=0;data=str(data)
    for i in range (0, len(data)):
        tmpData=tmpData+data[i]
        if start == 1:
            if data[i]==chr(44):start=start+1;i=i+1
            if start == 1:tmpData2=tmpData2+data[i]
            if start == 2:
                tmpData2=tmpData2.replace(':','')
                tmpData2=tmpData2.replace('"','')
                if tmpData == 'null': return ''
                return tmpData2
        if tmpData[-len(word):]== word:
            start=1
            if nb != 0: nb=nb-1; start=0;
        if i == len(data)-1:return ''

def verifTimeStamp(ts):
        if ts <  1388530800000:return 0
        localtime = time.localtime(time.time())
        stime= strftime('%Y-%m-%d %H', gmtime())
        date=datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H')
        if str(date) == str(stime): return 1;
        else: return 0
    
def timeStampToDate(ts):
        if ts <  1388530800000:return '2000-01-01 00:00:00'
        ts=ts/1000
        date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return date

def pTime():
    localtime = time.localtime(time.time())
    t = str(localtime.tm_hour)+":"+str(localtime.tm_min)+":"+str(localtime.tm_sec)
    return t

def timeStampToDelay(ts,ts2):
        delay=(ts2/1000-ts/1000)/60
        return delay


id_train=[]
t1= pTime()
l_stations=getStations()
getData(l_stations)
t2= pTime()
print t1+"   "+t2
