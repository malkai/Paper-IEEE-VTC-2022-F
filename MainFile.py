import json

import connect_firebase

n_leituras = 0

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
    
   
    vol_entrada = 400#!!!!!!!!valor chutado
    vol_nominal = 500#!!!!!!!!valor chutado
    
    Mol_ar = 28.96 #massa molar do ar
    
    #Equation (4) ? (5)
    eficenc_volumetrica = vol_entrada/vol_nominal

    V = 50 #the volume of the combustion chambers in the engine cylinders
   
    R = 8.3145 #the ideal gas constant J/ (mol*k)


    #Equation (14)
    massa_de_fluxo_de_ar = (Pressure_intake*V/(R*Temp_intake))*(Mol_ar*eficenc_volumetrica*RPM/120)


    #Equation (6)
    massa_co2 = massa_de_fluxo_de_ar*co2_per_gasoline/(AFR_gasoline*density_gasoline)
    
    return massa_co2


#Mass air Flow
def calc_co2(massa_de_ar):
    density_gasoline = 737  # Density of gasoline 737g/L
    density_diesel = 850  # Density of diesel 737g/L
    density_ethanol = 789  # Density of ethanol 737g/L

    co2_per_gasoline = 2310  # co2 per liter of gasoline g/L
    co2_per_diesel = 2660  # co2 per liter of diesel g/L
    co2_per_ethanol = 1519  # co2 per liter of ethanol g/L
    
    AFR_gasoline = 14.7  # AFR constant for gasoline
    AFR_diesel = 14.6  # AFR constant for diesel
    AFR_ethanol = 9.1  # AFR constant for ethanol
    
    massa_combustivel = massa_de_ar / AFR_gasoline
    
    massa_co2_p_l = massa_de_ar * co2_per_gasoline/(AFR_gasoline*density_gasoline)
    return massa_co2_p_l
    
def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


alldata =  {}

alldata = connect_firebase.getDoc()

#for doc in alldata:
    		#print('{} : {}'.format(doc.id,doc.to_dict()))

x = {doc.id: doc.to_dict() for doc in alldata}
#print(x)
json_object = json.dumps(x, indent = 4) 
print(json_object)
#print(y.to_dict()) 
#print(y.id,y.to_dict())
#for doc in x:
#    		print('{} : {}'.format(doc.id,doc.to_dict()))
#print(list(enumerate(alldata)))

#docs_dict = {doc.id:doc.to_dict() for doc in alldata}   
# print dictionary keys         

#def calculate_carbon_emissions():
    #for i in range(n_leituras):
        #co2_m1 = calc_co2_speed(measures["RPM"][i],measures["INTAKE_PRESSURE"][i],measures["INTAKE_TEMP"][i])
        #print(co2_m1)


  
    #for i in range(n_leituras):
        #co2_m2 = calc_co2(measures["MAF"][i])
        #print(co2_m2)