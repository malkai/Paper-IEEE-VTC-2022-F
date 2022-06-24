class Vehicle():
    def __init__(self, SPEED, RPM, INTAKE_TEMP, MAF, INTAKE_PRESSURE): #, THROTTLE_POS
       self.vin = '4TARN81P4RZ310448' 
       self.SPEED = SPEED
       self.RPM = RPM
       self.INTAKE_TEMP = INTAKE_TEMP
       self.MAF = MAF
       self.INTAKE_PRESSURE = INTAKE_PRESSURE
       #self.THROTTLE_POS = THROTTLE_POS

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'vin': '4TARN81P4RZ310448',
            u'SPEED': self.SPEED,
            u'RPM': self.RPM,
            u'INTAKE_TEMP': self.INTAKE_TEMP,
            u'MAF': self.MAF,
            u'INTAKE_PRESSURE': self.INTAKE_PRESSURE,
          #  u'THROTTLE_POS': self.THROTTLE_POS,
           
        }
        return dest
        # [END_EXCLUDE]


       
    def __repr__(self):
        return(
            f'Vehicle(\
                vin={self.vin}, \
                SPEED={self.SPEED}, \
                RPM={self.RPM}, \
                INTAKE_TEMP={self.INTAKE_TEMP}, \
                MAF={self.MAF}\
                INTAKE_PRESSURE={self.INTAKE_PRESSURE}, \
                )'
                 #THROTTLE_POS={self.THROTTLE_POS}\
           
        )


