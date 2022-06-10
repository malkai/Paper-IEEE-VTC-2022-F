import matplotlib
import matplotlib.pyplot as plt
import obd
import connect_firebase
import vehicle_status

connection = obd.OBD(portstr="/dev/pts/3")#se não estiver funcionando na pts/3, colocar na pts/2

measures = {

}
n_leituras = 2

def leitura(sensores,eh_mens):#a sensores são todos os sensores que são passados como parâmetro, e var se refere à variavel pra indicar se a lista é mensuravel ou n
    for cmd in sensores:
        qtd = 0
        leituras = []
        while (qtd < n_leituras):  # criar função leitura de sensor
            response = connection.query(cmd)
            if eh_mens == 1:
                a = response.value.magnitude
            else:
                a = response.value
            leituras.append(a)
            #print(a)
            #print("========================================")
            qtd += 1
        measures[cmd.name] = leituras
        #print(measures)

def print_graf(sensores ):
    for cmd in sensores:
        fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
        ax.set_xlabel('Tempo [s]')
        ax.set_ylabel(cmd.desc)
        ax.set_title(cmd.desc + " Por tempo")
        y = measures[cmd.name]
        x = range(n_leituras)
        ax.plot(x, y)

    ax.plot(x,y)
    plt.show()

def calc_co2(massa_de_ar):
    AFR = 14.7 #taxa de variação de fluxo de ar 14.7:1
    densidade_combustivel = 737  # densidade da gasolina 737g/L
    co2_per_liter = 2310  # co2 por litro da gasolina : 2310g/L
    massa_combustivel = massa_de_ar / AFR
    #volume_combustivel = massa_combustivel / densidade_combustivel

    #massa_co2_p_sec = volume_combustivel * co2_per_liter
    massa_co2_p_l = massa_de_ar * co2_per_liter/(AFR*densidade_combustivel)
    return massa_co2_p_l

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

mens = 1
inmens = 0

cmd_mens = [
    obd.commands.SPEED,
    obd.commands.RPM,
    obd.commands.INTAKE_TEMP,
    obd.commands.MAF,
    #obd.commands.FUEL_PRESSURE, #comando insdisponível
    obd.commands.INTAKE_PRESSURE,
]

cmd_inmens = [
    obd.commands.THROTTLE_POS,
    #obd.commands.AMBIANT_AIR_TEMP, #comando insdisponível
    #obd.commands.ETHANOL_PERCENT, #comando indisponível
    #obd.commands.FUEL_RATE,
]

leitura(cmd_mens, mens)
#print_graf(cmd_mens)

leitura(cmd_inmens, inmens)
#print_graf(cmd_inmens)

#print("CO2 calculado: ")

for i in range(n_leituras):
    co2_m1 = calc_co2_speed(measures["RPM"][i],measures["INTAKE_PRESSURE"][i],measures["INTAKE_TEMP"][i])
    #print(co2_m1)


# fechar os graficos gerados pelo matplotlib para mostrar o quanto de CO2 foi consumido
print('====================================================================================================')

for i in range(n_leituras):
    co2_m2 = calc_co2(measures["MAF"][i])
    #print(co2_m2)

for i in range(n_leituras):
    a = vehicle_status.Vehicle(measures["SPEED"][i],measures["RPM"][i],measures["INTAKE_TEMP"][i],measures["MAF"][i],measures["INTAKE_PRESSURE"][i])#measures["THROTTLE_POS"][i]
    print(a)
    print('\n')
    print(i)
    connect_firebase.insertele(a)

