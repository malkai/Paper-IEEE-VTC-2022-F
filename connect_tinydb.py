from __future__ import annotations
from concurrent.futures.process import _threads_wakeups
import csv
from tinydb import TinyDB
import os.path
import json
from vahiclehelp import Vehicle_Help
import calculation_co2
import datetime 
from datetime import datetime 
import haversine
from haversine import haversine
import matplotlib.pyplot as plt
import numpy as np

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
                level = data[i]['obdData']['01 2F']['response']
                if(len(vin)==17):
                    #co2 = data[i]['obdData']['01 10']['response']
                    
                    co2 = calculation_co2.calc_co2_speed(float(rpm), float(kpa), float(temp_air))
                    if(co2!=0):
                        help_var = Vehicle_Help(vin, hash, co2, times_tamp,lat, lon,level,temp_air)
                        y.append(help_var)
                else:  
                    print('Error '+hash) 
            except:  
                    a =1    
           
        db = TinyDB('db.json')
        for doc in y:
            db.insert({'vin':doc.vin,'hash':doc.hash,'co2':doc.co2,'times_tamp':doc.data,'lat':doc.lat,'lon':doc.lon, 'percent':doc.level, 'temp_air':doc.temp})
          


def plot_information(total_vin):
    for i in total_vin:
            plt.plot(i[1],i[2])
            plt.grid()
            plt.title("Medida percorrida "+ i[0])
            plt.xlabel("Tempo em segundos(s)")
            #plt.ylabel("Quilómetros(KM)")
            plt.ylabel("Porcentagem(KM)")
            #plt.set_ylim([,])
            #plt.xticks(np.arange(,,15))
            #print(i[3])
            #plt.axis((min(i[1]), max(i[1]), min(i[2]), max(i[2])))
            plt.show()


def print_veh():
    db = TinyDB('db.json')
    ah = db.all()
    ah.sort(key=lambda x:(x['vin'], x['times_tamp']), reverse=False)
    
    time_y = []
    km_x = []
    total_vin = []
    percent = []
    
    vin = ''
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    temp_day = ''
    result= ''
    
    soma_time = 0 
    soma_km = 0
    harv=0
   
    ''' 
    with open('carros.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            
            # write multiple rows
            for i in ah:
                aux = (i['vin'],i['times_tamp'],i['percent'],i['temp_air'])
                writer.writerow(aux)'''

    
    for h1 in ah:
       
        if temp_day=='':
            temp_day = datetime.strptime(h1['times_tamp'], fmt)
            cord_ant=(h1['lat'],h1['lon'])
            vin = h1['vin'] 
        
        time_after = datetime.strptime(h1['times_tamp'], fmt)
        cord_prox=(h1['lat'],h1['lon']) 

        harv_ant = harv
        harv = haversine(cord_ant,cord_prox)
        #print(harv_ant,harv,harv_ant-harv)
        if harv-harv_ant!=0: 
            result =   temp_day - time_after
           
           
            if result.seconds<=60:
          
                
                         
                if 0 not in km_x:
                    time_y.append(0)   
                    km_x.append(0.0) 
                    percent.append(0.0) 
                else:
                    soma_km += harv
                    soma_time += result.seconds 
                    time_y.append(soma_time)   
                    km_x.append(soma_km) 
                    percent.append(h1['percent'])
                      
                  
           
            else:  
                
                if len(time_y)>1 and len(km_x)>1:
                    total_vin.append([vin, time_y[:],km_x[:],percent[:]]) 
                print(total_vin)     
                vin = h1['vin'] 
                temp_day = ''
                soma_time = 0
                soma_km = 0 
                result = ''    
                time_y.clear()
                km_x.clear()
                percent.clear()
        else:  
            result =   temp_day - time_after
            soma_time += result.seconds 
            time_y.append(soma_time)   
            km_x.append(soma_km) 
            percent.append(h1['percent'])
                      
                  
           
        temp_day = time_after
        cord_ant = cord_prox   
                
        
        if  vin!=h1['vin'] or h1==ah[-1]:
            if len(time_y)>1 and len(km_x)>1:
                total_vin.append([vin, time_y[:],km_x[:],percent[:]])
            vin = h1['vin']
            temp_day = ''
            soma_time = 0
            soma_km = 0 
            result = ''
           
            time_y.clear()
            km_x.clear()
            percent.clear()
    
    #for i in total_vin:
    #    if(i[0]=='9BHBG51DAEP106133'):    
    #        print(i)
    #plot_information(total_vin)

           
         
