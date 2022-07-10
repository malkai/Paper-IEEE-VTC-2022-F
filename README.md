# The Project

Does this repository contain the implementation of the Crowdsourcing and Monetization Strategy to increase Energy Efficience in Vehicles Mobility. It was developed on INMETRO to gather the emission of carbon from vehicles with an OBD2 scanner. This software will be essential for manufacturers when they need to curb their carbon. 

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



# 1. Installing dependencies
In this last endpoint it will be possible to close the order for new bids, at its closing the respective balance is computed for the owner and the last bidder of the order, this order will also be closed for new bids.
```console
./installFabric.sh
```

**Observation**: It is not necessary to run the script as *sudo*, only when necessary it will ask for permission along with your password.

# 2. Generating MSP artifacts

First you need to check the variable FABRIC_CFG_PATH, uncomment it at [configmsp.sh](nmiblocknet\configmsp.sh)

```console
export FABRIC_CFG_PATH=$PWD
```

After that run the script:

```console
./configmsp.sh
```

This script generates the MSP certificates in the folder crypto-config which must be replaced in  [ptb.de.json](nmiblocknet\fabpki-cli\ptb.de.json) and [inmetro.br.json](nmiblocknet\fabpki-cli\inmetro.br.json) on lines 38,39,51

# 3. Managing docker containers

Let's then check the contents in the folder [.env](nmiblocknet\.env), access it and change it according to your IP address. We must also access [ptb.de.json](nmiblocknet\fabpki-cli\ptb.de.json), [inmetro.br.json](nmiblocknet\fabpki-cli\inmetro.br.json) and modify on lines 58,76,77 with your machine IP address. If you want you can keep the default port *(:7050 / :7051 / :7053)*.

To start the container of a specific organization use the command:

```console
docker-compose -f peer-ptb.yaml up -d
```

If your organization is responsible for hosting the orderer service, you will also need to initiate it with your organization, informing both files .yaml:

```console
docker-compose -f peer-orderer.yaml -f peer-ptb.yaml up -d
```

If it is necessary to disable or restart the containers, use the following commands: 

For stoping the containers:
```console
docker-compose -f peer-ptb.yaml stop
```

For resseting the containers:
```console
./teardown.sh peer-ptb.yaml
```

# 4. Create Fabric connection and connect peers

To make this connection run the following command, changing the organization only if necessary:

```console
./configchannel.sh ptb.de -c
```

If successful, Hyperledger Fabric will be running on your server, with an instance of your organization on the system. To see more information about the container run:

```console
docker ps
docker stats
```

# 5. Installing and instance chaincode

Insert the chaincode inside the folder [fabpki](nmiblocknet\fabpki-cli), go back to the project root folder and run the following command to install the chaincode:

```console
./configchaincode.sh install cli0 fabpki 1.0
```

To instantiate the chaincode across the network run the command: 

```console
./configchaincode.sh instantiate cli0 fabpki 1.0
```

# 6. Some more dependencies


Let's install some more dependencies needed to run the next code:

```console
cd $HOME
git clone https://github.com/hyperledger/fabric-sdk-py.git
cd fabric-sdk-py
git checkout tags/v0.8.0
sudo make install
```

```console
cd $HOME
git clone https://github.com/hyperledger/fabric-sdk-py.git
cd fabric-sdk-py
git checkout tags/v0.8.0
sudo make install
```

# 7. Starting API 

Run the API [ledgerRequest.py](nmiblocknet\fabpki-cli\ledgerRequest.py) with:

```console
python3 requisicaoAPI.py
```

Your terminal will show two IP addresses. Generally, in a local environment, the *127.0.0.1 (same as localhost)*, however, if you want to make requests outside your local environment, you must use the IP of your network.

# 8. Fazendo requisições 


Install Insomnia or any other environment for testing HTTPS requests, if you use Insomnia import the file [backup-insomnia.json](nmiblocknet\extras\backup_insomnia.json), if you don't have Insomia, you can check the body of requests just by the JSON file.


### How to make a POST of Information
![Post Vehicle](https://i.imgur.com/4tInvyv.png)

This is the body needed to insert a vehicle into the network, notice that there is a parameter called "Vin", it is super important because it is necessary for the registration of manufacturers within the network, so make sure that this Vin is a valid parameter to avoid conflicts.

### How to make a POST of Manufacturer
![Post Manufacturer](https://i.imgur.com/Pgy0EKm.png)

At first it will not be necessary to use this endpoint, as manufacturers are automatically entered when verifying the vehicle manufacturer, this is done so that vehicle credits are not lost if the vehicle manufacturer does not exist on the network.

### How to make a POST of Balance on ledger
![Post Sold](https://i.imgur.com/JRuZKoZ.png)

This endpoint is used so that the amount of accumulated Co2 from the manufacturers is converted into a balance based on a target, in a system issue this endpoint must be activated at equidistant periods for a more accurate sampling of these calculations.

# 9. Auction

After calculating the balance of manufacturers, it will be possible to start transactions within the system, where manufacturers with a negative carbon balance can buy the balance of other manufacturers with a fiat currency. Everyone starts with 10,000 of this fiat currency for testing.

## POST - Start an order
![Post Start an order](https://i.imgur.com/4tJI6WV.png)

With this endpoint it is possible to start a new *order*. As a parameter we have the owner of the order, which will come with the id of the manufacturer within the blockchain records *(In this network, the entire manufacturer starts with "fab-")*. We have the purchase type, being authorized with "seller" and "seller". The last one offered, if filled in "with balance to buy" in the balance balance type field, this balance balance, if filled in "sell" will represent the balance of the carbon balance

## POST - Register an bid
![Post bid](https://i.imgur.com/BCfamAP.png)

This endpoint represents a bid within the previously created order. It has the created transaction id in its JSON body *(There is a GET endpoint for transactions in Insomnia's backup JSON)*. The amount of your bid, with the details in case the order is a sell or buy order explained in the previous item. Lastly, the buyer id.

There are some business rules within the system, such as the impossibility of placing two bids in a row for the same manufacturer, or even placing a bid with insufficient balance. Watch out for that!

## POST - Close an order
![Post close order](https://i.imgur.com/N4Byu8p.png)

In this last endpoint it will be possible to close the order for new bids, at its closing the respective balance is computed for the owner and the last bidder of the order, this order will also be closed for new bids.

