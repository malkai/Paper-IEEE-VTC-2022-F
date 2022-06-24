import connect_firebase

n_leituras = 0


# Speed density:
def calc_co2_speed( RPM, Pressure_intake, Temp_intake):
    densidade_combustivel = 737  # densidade da gasolina 737g/L
    co2_per_liter = 2310  # co2 por litro da gasolina : 2310g/L
    AFR = 14.7  # taixa de variação de fluxo de ar 14.7:1

    ########SPEED DENSITY########
    vol_entrada = 400#!!!!!!!!valor chutado
    vol_nominal = 500#!!!!!!!!valor chutado
    Mol_ar = 28.96 #massa molar do ar
    eficenc_volumetrica =vol_entrada/vol_nominal

    V = 50 #!!!!!!!!valor chutado
    R = 8.3145
    #T = obd.commands.INTAKE_TEMP#no artigo fala intake abolute temp, mas só tem a função de intake air temp
    massa_de_fluxo_de_ar = (Pressure_intake*V/(R*Temp_intake))*(Mol_ar*eficenc_volumetrica*RPM/120)
    massa_co2 = massa_de_fluxo_de_ar*co2_per_liter/(AFR*densidade_combustivel)
    return massa_co2


#Mass air Flow
def calc_co2(massa_de_ar):
    AFR = 14.7 #taxa de variação de fluxo de ar 14.7:1
    densidade_combustivel = 737  # densidade da gasolina 737g/L
    co2_per_liter = 2310  # co2 por litro da gasolina : 2310g/L
    massa_combustivel = massa_de_ar / AFR
    #volume_combustivel = massa_combustivel / densidade_combustivel

    #massa_co2_p_sec = volume_combustivel * co2_per_liter
    massa_co2_p_l = massa_de_ar * co2_per_liter/(AFR*densidade_combustivel)
    return massa_co2_p_l

#def calculate_carbon_emissions():
    #for i in range(n_leituras):
        #co2_m1 = calc_co2_speed(measures["RPM"][i],measures["INTAKE_PRESSURE"][i],measures["INTAKE_TEMP"][i])
        #print(co2_m1)


  
    #for i in range(n_leituras):
        #co2_m2 = calc_co2(measures["MAF"][i])
        #print(co2_m2)




connect_firebase.getDoc()