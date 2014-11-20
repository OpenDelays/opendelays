#!/usr/local/bin/python
# -- coding: utf-8 --

##### ------ OpenDelays v1.1------ #####

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

def tts(ttsIndex): #tts for text to search
    dep="TrainStation Green"
    depT="StationColumnTime"
    delay="StationColumnDelay"			
    dest="StationColumnName"
    track="StationColumnTrack"
    trainType="StationColumnType"
    trainNumber="StationColumnNumber"

    if ttsIndex == 0:
            text=dep
    if ttsIndex == 1:
            text=depT
    if ttsIndex == 2:
            text=delay
    if ttsIndex == 3:
            text=dest
    if ttsIndex == 4:
            text=track
    if ttsIndex == 5:
            text=trainType
    if ttsIndex == 6:
            text=trainNumber
    return text

def urlCalculate(urlParam, timeParam):#urlParam corresponding with the train station index
    #open website page
    #http://www.railtime.be/website/ShowStation.aspx?l=FR&smc=1&stat=253&stl=DE&dep=1&tr=17:00-60&stn=0&pid=ssid
    siteRailTime = ''
    siteRailTime1 = 'http://www.railtime.be/website/ShowStation.aspx?l=FR&smc=1&stat='
    siteRailTime2 = '&stl=DE&dep=1&tr='
    siteRailTime3 = '-60&stn=0&pid=ssid'
    siteRailTime=str(siteRailTime1)+str(urlParam)+str(siteRailTime2)+ str(timeParam)+str(siteRailTime3)
    return siteRailTime
	
def pdiod(l_Data,nbf): #put data in other document in csv format (take 2d list and number of found element)
    f = open ('test.txt','a')
    for m in range (1,nbf): #m is an index for data in one category
            for n in range (0,7): #n is an index for category -- relative to tts index
                    f.write(l_Data[n][m])
                    if n != 6 :f.write(',') #to respect csv format
            f.write('\n')
    f.close()        

def wTime():
    f=open("project/info.txt","a")
    localtime = time.localtime(time.time())
    t = str(localtime.tm_hour)+":"+str(localtime.tm_min)+":"+str(localtime.tm_sec)
    f.write(t+'\n')
    f.close()

def pdidb(l_Data,nbf): #put data in database
    db = Database() #init class database and attributes
    for m in range (1,nbf):
        if len(l_Data[2][m])>1: #to cast variable into time format for db
            delay=l_Data[2][m]
            delay=delay[len(delay)-5:]
            l_Data[2][m]=delay        
        # Data Insert into the table
        #prepare Query
        query1 = """
            INSERT INTO opendelays_railtime
            (`departure`, `datetime`, `delay`, `destination`, `track`, `trainType`, `trainNum`)
            VALUES"""
        query2="('"+l_Data[0][m]+"','"+l_Data[1][m]+"','"+l_Data[2][m]+"','"+l_Data[3][m]+"','"+l_Data[4][m]+"','"+l_Data[5][m]+"','"+l_Data[6][m]+"')"
        query=query1+query2
        db.insert(query)

def search(urlToSearch):
    l_Index=[[],[],[],[],[],[],[]] #we're going to put search data in this list of 8 elements
    i=0 #file index
    j=0 #text index
    nbf=0 #number of found series of data
    verif=0 #verification variable to be sure we found the good word
    tampon='' #tmp value of compared string with text
    tampon2='' #tmp value of search data 
    ttsIndex=0
    localtime = time.localtime(time.time())
    day=int(time.strftime("%d"))-1
    if str(localtime.tm_hour-1)=="23":date=time.strftime("%Y-%m-")+str(day)
    else: date=time.strftime("%Y-%m-%d")
    page=urllib.urlopen(urlToSearch) #access to url we calculate before
    #print 'We are on : '+urlToSearch+'\n'

    strpage = page.read() #reading doc assigned to a tmp variable
    strpage = strpage.replace(chr(13), "")
    sizef = len(strpage)-1 #length of file
    for i in range (0,sizef): #in file :
            
            text=tts(ttsIndex) #call function to calculate which text we're looking for
            size=len(text) #length of text
            for j in range (0,size): #in word/sentence :
                    if (i+j<sizef and strpage[i+j]==text[j]): #if the letter we read is the same of the letter we search 
                            tampon=tampon+strpage[i+j] #save the letter in a tmp variable
                            if len(tampon) == size: #if the length of the tmp variable is the same of the text we analyse the content
                                    for l in range (0,size):#check all letters to confirm if the text found is the text we want
                                            if tampon[l]==text[l]: 
                                                    verif=verif+1 
                                    if verif==size: #we find the text in file -> variables go back to originals value
                                            tampon=''
                                            verif=0
                                            #init variables for next step
                                            n=i+j
                                            bChevron=False
                                            nbChevron=0
                                            while bChevron == False: #while char isn't '>' continue to read
                                                    n=n+1
                                                    if strpage[n] == chr(62) and text!="StationColumnName":bChevron=True
                                                    if nbChevron == 1 and strpage[n] == chr(62):bChevron=True
                                                    if strpage[n] == chr(62) and text=="StationColumnName" and strpage[n+1] == chr(32):nbChevron=nbChevron+1 #location of those data aren't like the other
                                                    if strpage[n] == chr(62) and text=="StationColumnName" and strpage[n+1] != chr(32):bChevron=True #data in international travel aren't in the same format
                                                    if nbChevron == 2:bChevron=True #end of loop, we find data index in file
                                                    #we are on the good location -> save data
                                            if text=='TrainStation Green':n=n+10 #Exception : departure station is needed once for all file
                                            while strpage[n] != chr(60): #while next char isn't '<' save him in tampon2
                                                    n=n+1
                                                    tampon2=tampon2+strpage[n]
                                            tampon2=tampon2[0:len(tampon2)-1] #formatting data
                                            if text=='StationColumnTime':l_Index[ttsIndex].append(date+" "+tampon2)
                                            else :l_Index[ttsIndex].append(tampon2) #add data to list
                                            tampon2='' #variable go back to originals value
                                            ttsIndex=ttsIndex+1
                                            if ttsIndex == 7: #switch text
                                                    ttsIndex=1
                                                    nbf=nbf+1
                    else: #if the letter isn't the one we search, go to next char in file
                            tampon=''
                            j=size
    for k in range (1,nbf):
            l_Index[0].append(l_Index[0][0]) #departure station
            delayV=l_Index[2][k]
            if delayV[0] != '+':
                    l_Index[2][k]=' ' # delete "&nbsp" elements, corresponding to "no delay"
   # pdiod(l_Index,nbf) #call function to write all found data in csv format
    pdidb(l_Index,nbf)
	
#declaration of global variables
urlToSearch=''
text=''
param1Max = 1969
localtime = time.localtime(time.time())
timeParam = str(localtime.tm_hour-1)+":00"
#wTime()
for urlParam in range(0,param1Max):
    url=urlCalculate(urlParam,timeParam)
    search(url)
#wTime()
#print '\n fin de la recherche'

