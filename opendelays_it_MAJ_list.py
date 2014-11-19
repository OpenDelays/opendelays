import urllib

f=open("project/stations-trains.txt","w")

for i in range (0,40000):
    u="http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+str(i)
    s= urllib.urlopen(u).read()
    if len(s) > 10 :f.write(s+"\n")
    #print str(i)+" / 10000"
f.close()
