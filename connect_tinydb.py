from __future__ import annotations
from xml.dom.minidom import Document
from tinydb import TinyDB, Query
import os.path
import json
from vahiclehelp import Vehicle_Help
import calculation_co2
import csv
import datetime 
from datetime import datetime, timedelta
import time
import geopy.distance

def createDb():
    y =[] 
    db =''
    file_exists = os.path.exists('json_data.json')
    
    if(file_exists):
        f = open('json_data.json')
        data = json.load(f)
        for i in data:
            
  
            try:
                vin = data[i]['obdData']['09 02 5']['response']
                hash = i
                times_tamp = data[i]['timeStamp']
                lat = data[i]['position']['lat']
                lon = data[i]['position']['long']
                kpa = data[i]['obdData']['01 0B']['response']
                temp_air = data[i]['obdData']['01 0F']['response']
                rpm = data[i]['obdData']['01 0C']['response']
               
                if(len(vin)==17):
                    #co2 = data[i]['obdData']['01 10']['response']
                    
                    co2 = calculation_co2.calc_co2_speed(float(rpm), float(kpa), float(temp_air))
                    if(co2!=0):
                        help_var = Vehicle_Help(vin, hash, co2, times_tamp,lat, lon)
                        y.append(help_var)
                else:  
                    print('Error '+hash) 
            except:  
                    a =1    
           
        db = TinyDB('db.json')
        for doc in y:
            db.insert({'vin':doc.vin,'hash':doc.hash,'co2':doc.co2,'times_tamp':doc.data,'lat':doc.lat,'lon':doc.lon})
            #if(data[i].get('userId') != 'None'):
            #    print('teste')
        #db = TinyDB('db.json')
    #print(db.all())

#def insertDb():
vin = ''
co2_total = 0

hash = ''
    
def searchDb():
    db = TinyDB('db.json')
    Todo = Query()
    y = []
    y1 = []
    vin = ''
    co2_total = 0
    temp_day = ''
  
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    ah = db.all()
    for doc in ah:
        if(doc['vin'] not in y):
           y.append(doc['vin'])
    
    for h1 in y:
        print(h1)  
        ah = db.search(Todo['vin']==h1)
        vin = h1
        ah.sort(key=lambda x:(x['vin'], x['times_tamp']), reverse=True)
        co2_total = 0
        result= 0 
        menor = 0
        km = 0
        new_value =0 
        help_time = 0
        temp_day='' 
        ant = 0
        pos = 0
        for doc in ah:
            if(doc['vin']=='93HGK5870GZ218968'):
                print(doc['vin'],doc['times_tamp'],doc['co2'])
            if(temp_day==''):
                temp_day = datetime.strptime(doc['times_tamp'], fmt)
                cord1=(doc['lat'],doc['lon'])
                co2_total += doc['co2'] 
            
            time_after = datetime.strptime(doc['times_tamp'], fmt)
            
            if(temp_day > time_after ):
                ant = pos
                pos = (temp_day-time_after).total_seconds()/60
                
                if(pos-ant>0 and pos-ant<1):
                    #print(pos-ant)
                #menor = datetime.strptime(doc['times_tamp'], fmt)
                    menor = result
                    #print(doc['co2'],co2_total)
                   
                    co2_total += doc['co2']
                    help_time += (pos-ant) 
                #print(menor)
                    result = (temp_day -time_after).total_seconds()
                    cord2 = (doc['lat'],doc['lon'])
                    old_value = new_value
                    new_value = geopy.distance.geodesic(cord1, cord2).km
                    if(old_value != new_value and (result- menor) / 60>0 ):
                    #print(cord1,cord2)
                        #print(cord1,cord2,geopy.distance.geodesic(cord1, cord2).km) 
                        km += geopy.distance.geodesic(cord1, cord2).km
                        cord1 = cord2
            
                    if(result>1000):
                        y1.append([vin,doc['times_tamp'],co2_total,km,help_time])
                        temp_day = ''
                        cord1=cord2
                        co2_total = 0
                        km = 0
                        help_time=0
              
                
               
                
                #print(result/60)
                #print(cord1,cord2)    
                  
        km += geopy.distance.geodesic(cord1, cord2).km 
        if(temp_day!=''):
            y1.append([vin,doc['times_tamp'],co2_total,km,help_time])

                
    #for doc in y1:
       #print(doc)
           
            #if(result!=0):

            #print(result // 60)
            #if(temp_day > doc['times_tamp']):

            #    print('oi')
    with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)


        
        # write multiple rows
        writer.writerows(y1)                
             

'''
                
    #sorted(ah, key=lambda x: x['Age'], reverse=True)
    for i in ah:
            
            print(i['co2'])
            if(tempo_dia==''):
                tempo_dia = i['times_tamp'][0:10]    
            co2_total += i['co2']
            
        y1.append([vin,tempo_dia,co2_total])
        tempo_dia = ''
        co2_total = 0

    with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)


        
        # write multiple rows
        writer.writerows(y1)

class carro_tabela
    vin 
    hash
    co2
    está no mesmo dia mes e ano 
    se o tempo está que 15 min o carro está parado inicia uma nova medição
    total de kilometro percorridos
    kmfinal
    {
    lat_min
    lon_min
    lat_max
    lon_max
    }
'''