import json
from subprocess import check_output
import connect_firebase
from vehicle import Vehicle

'''
# Speed density:
def calc_co2_speed( RPM, Pressure_intake, Temp_intake):
    

    density_gasoline = 737  # Density of gasoline 737g/L
    density_diesel = 850  # Density of diesel 737g/L
    density_ethanol = 789  # Density of ethanol 737g/L

    co2_per_gasoline = 2310  # co2 per liter of gasoline g/L
    co2_per_diesel = 2660  # co2 per liter of diesel g/L
    co2_per_ethanol = 1519  # co2 per liter of ethanol g/L
    
    AFR_gasoline = 14.7  # AFR constant for gasoline
    AFR_diesel = 14.6  # AFR constant for diesel
    AFR_ethanol = 9.1  # AFR constant for ethanol
    
    #Vintake represents the real volume of intake air supported by the cylinders.
    Vintake = 400#!!!!!!!!valor chutado
   
    #Vnominal is the theoretical volume of the engine.
    Vnominal = 500#!!!!!!!!valor chutado
    
    mass_air = 28.96 #massa molar do ar
    
    #Equation (12)
    #On the article the value volumetric eficiency
    volumetric_efficiency = 0.8
    
    #the volume of the combustion chambers in the engine cylinders
    V = 50
    #the ideal gas constant J/ (mol*k)
    R = 8.3145 

    #Pressure_intake represents the pressure in the combustion chamber and can be obtained by means of the MAP (Manifold Absolute Pressure) sensor in KPa.
    #Temp_intake T is the gas temperature. It can be obtained by the IAT (Intake Absolute Temperature) sensor in K.
    
    #Equation (14)
    mass_of_air_flow = (Pressure_intake*V/(R*Temp_intake))*(mass_air*volumetric_efficiency*RPM/120)


    #Equation (6)
    mass_co2 = mass_of_air_flow*co2_per_gasoline/(AFR_gasoline*density_gasoline)
    
    return mass_co2
'''

#Mass air Flow
def calc_co2(air_mass):
    density_gasoline = 737  # Density of gasoline 737g/L
    density_diesel = 850  # Density of diesel 737g/L
    density_ethanol = 789  # Density of ethanol 737g/L

    co2_per_gasoline = 2310  # co2 per liter of gasoline g/L
    co2_per_diesel = 2660  # co2 per liter of diesel g/L
    co2_per_ethanol = 1519  # co2 per liter of ethanol g/L
    
    AFR_gasoline = 14.7  # AFR constant for gasoline
    AFR_diesel = 14.6  # AFR constant for diesel
    AFR_ethanol = 9.1  # AFR constant for ethanol
    
    mass_fuel = air_mass / AFR_gasoline
    
    #Equation (6)
    massa_co2_p_l = air_mass * co2_per_gasoline/(AFR_gasoline*density_gasoline)
    return massa_co2_p_l
    
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

alldata = connect_firebase.getDoc()


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
        id = doc.id
        #print('')
       
        #print(var_vali)
        
        try:
            velocity = doc.get('obdData.`01 0D`.response')
        except:          
            var_vali = False
            #print("Not found velocity")
        
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
            MAF_var = doc.get('obdData.`01 10`.response')
            
        except:
            var_vali = False
            #print("Not found MAF")
     
        var_vali = validate(MAF_var)
      
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
            #print("Not found RPM") 
        
        var_vali = validate(vin)            
       
        if(var_vali == True and MAF_var!=''and MAF_var!=0):

            calc_2 = calc_co2(float(MAF_var))
        
        
        var_vali = True 
        if(calc_2!=0):
            aux_carro = Vehicle(vin,id,calc_2,velocity)
            y.append(aux_carro)


#connect_firebase.change_flag(y)        