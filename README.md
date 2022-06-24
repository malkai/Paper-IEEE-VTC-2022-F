

# The Project

Does this repository contain the implementation of the ?NAME?It was developed on INMETRO to gather the emission of carbon from vehicles with an OBD2 scanner. This software will be essential for manufacturers when they need to curb their carbon. 

 Research team:

Malkai dos S. P. Oliveira (omalkai14@gmail.com)

Kauã Cassino (kauacassiano121@gmail.com)

Coordination:

Paulo Nascimento (prnascimento@inmetro.gov.br)

Wilson S. Melo Jr. (wsjunior@inmetro.gov.br)




# What the Project is



To achieve better fuel efficiency and to reduce CO2 emissions, the volume of air penetrating the engine must be calculated. In this program, we calculate the amount of CO2 emission.


For the variable we essentially use 3 variables they are:


Mass Air Flow rate (MAF)

Manifold Air Pressure (MAP)

air intake temperature



The Mathematical methods used in this work were: 

**Mass air Flow**:
This method directly uses the Mass Air Flow (MAF) sensor present in the vehicles to obtain the reading of airflow. The value obtained is in the unit mass/time.

**Speed density**:
This method performs an estimation of the air mass based on the ideal gas law. To do this, it uses readings of temperature and air pressure sensors in the vehicle, in addition to using the volumetric efficiency of the engine. This method can be used with the MAP sensor, as it measures the absolute pressure.

In a brief comparison between both of them, one can show the speed of density method has greater mathematical complexity than the mass air flow method. It is possible because one needs a combination of sensors to calculate the desired estimations indirectly, whereas the mass air flow method directly uses the MAF sensor to do the same. Although the MAF sensor could not be found in all vehicles.

In this project we had some volunteers,  who gave us essential information about the vehicle by an OBD2 device, The device was gathering the information and sent it to our database, we used the language python to obtain all information and send it to our API, this API check the information and save the data on Blockchain. 


