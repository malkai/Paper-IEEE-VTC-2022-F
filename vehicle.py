class Vehicle():
    def __init__(self, VIN, HASH,  CO2, VELOCITY): #, THROTTLE_POS
       self.vin = VIN
       self.hash = HASH
       self.co2 = CO2
       self.velocity = VELOCITY
      

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'vin': self.vin,
            u'HASH': self.hash,
            u'CO2': self.co2,
            u'TIMESTAMP': self.velocity,
        
           
        }
        return dest
        # [END_EXCLUDE]


       
    def __repr__(self):
        return(
            f'Vehicle(\
                vin={self.vin}, \
                HASH={self.hash}, \
                CO2={self.co2}, \
                TIMESTAMP={self.velocity},\
                )'
            )


