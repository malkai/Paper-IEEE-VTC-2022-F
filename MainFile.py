import json
from subprocess import check_output
from Requestinformation import post_information
import connect_firebase
import connect_tinydb
from vehicle import Vehicle
import json
import calculation_co2

#in this function we only acknowledge gasoline for make the math
# Speed density:

def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def validate (x):
    if x and x.strip():
        #myString is not None AND myString is not empty or blank
        return True
    #myString is None OR myString is empty or blank
    return False

alldata =  {}
y = []
var_vali = True 

connect_tinydb.print_veh()
#alldata = connect_firebase.getDoc()
#alldata = {'a','b','c'}
#x = {doc.id: doc.to_dict() for doc in alldata}
#json_object = json.dumps(x, indent = 4) 
#with open('json_data.json', 'w') as f:
#      f.write(json_object)
    
'''
for doc in alldata:
       
        calc_1 = 0
        calc_2 = 0
        x = '' 
        velocity = ''
        kPa = ''
        temp_air = '' 
        MAF_var = ''
        RPM_var = ''
        vin = ''
        data = ''
        id = doc.id
        print(id)   
        try:
            velocity = doc.get('obdData.`01 0D`.response')
        except:          
            var_vali = False
            #print("Not found velocity")
        
        var_vali = validate(velocity)
        
        try:
            data = doc.get('timeStamp')
        except:          
            var_vali = False
            #print("Not found data")
        
        var_vali = validate(velocity)

        try:
            kPa = doc.get('obdData.`01 0B`.response')  
        except:
            var_vali = False
            #print("Not found kPa")   
        
        var_vali = validate(kPa)      
        try:
            temp_air = doc.get('obdData.`01 0F`.response')
        except:           
            var_vali = False
            #print("Not found temperature air")  
        
        var_vali = validate(temp_air)

        
        try:
            RPM_var = doc.get('obdData.`01 0C`.response')
            
        except:
            var_vali = False
            #print("Not found RPM") 
        
        var_vali = validate(RPM_var)
        
        try:
            vin = doc.get('obdData.`09 02 5`.response')
            
        except:
            var_vali = False
            #print("Not found vin") 
        
        var_vali = validate(vin)            
               
        
        
        
        try:
            MAF_var = doc.get('obdData.`01 10`.response')
            
        except:
            var_vali = False
            print("Not found MAF")
        
        var_vali = validate(MAF_var)
        
      
        try:
           calc_1 = calc_co2_speed(float(RPM_var),float(kPa),float(temp_air))
            
        except:
            a = 1
                
        var_vali = True 

        if(calc_1!=0):
            aux_carro = Vehicle(vin,id,calc_1,data)
            y.append(aux_carro)
'''


#y.sort(key=lambda x:(x.vin, x.data), reverse=True)
#for doc in y:
#    print(doc)

  
    
#post_information(y)
#connect_firebase.change_flag(y)        