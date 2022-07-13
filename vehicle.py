class Vehicle():
    def __init__(self, VIN, HASH,  CO2, DATA, LAT, LON): #, THROTTLE_POS
       self.vin = VIN
       self.hash = HASH
       self.co2 = CO2
       self.data = DATA
       self.lat = LAT
       self.lon = LON
      

    def obd_dict__(self):
        # [START_EXCLUDE]
        dest = {
            u'VIN': self.vin,
            u'HASH': self.hash,
            u'CO2': self.co2,
            u'DATA': self.data,
            u'LAT': self.lat,
            u'DATA': self.lon,
               
        }
        return dest
        # [END_EXCLUDE]


       
    def __repr__(self):
        return(
            f'Vehicle(\
                VIN={self.vin}, \
                HASH={self.hash}, \
                CO2={self.co2}, \
                DATA={self.data}, \
                LAT={self.lat}, \
                LON={self.lon}, \
                )'
            )


