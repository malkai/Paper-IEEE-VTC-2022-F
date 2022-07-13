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
    Vintake = 400#
   
    #Vnominal is the theoretical volume of the engine.
    Vnominal = 500#
    
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
    mass_of_air_flow = (Pressure_intake*V/(1000*R*Temp_intake))*mass_air*volumetric_efficiency*(RPM/120)


    #Equation (6)
    mass_co2 = mass_of_air_flow/(AFR_gasoline*density_gasoline)*co2_per_gasoline
    
    return mass_co2


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
    mass_co2_p_l = air_mass/(AFR_gasoline*density_gasoline) * co2_per_gasoline
    return mass_co2_p_l
    