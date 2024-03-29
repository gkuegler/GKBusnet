#main base level device class
import modbus_client as client
import time
import random
import threading as th

default_reg_vals = [44,None,None]
class timeoutexcept(Exception): pass

class Device(client.ModbusClient):
    
    def __init__(self, name, host=None, port=None, debug=False, pollfreq=3, reg1=None, reg2=None, reg3=None):
        super(Device, self).__init__(host=host, port=port)
        self.name = name
        self.pollfreq = pollfreq
        self._can_update = False
        self.comprotocol = 'ModbusTCP'
        self.status = 'trying...'
        self.reg1, self.reg2, self.reg3 = default_reg_vals
        self.reg1_type, self.reg2_type, self.reg3_type = reg1, reg2, reg3
        self.error = None
        self.timeout = 10
        self._testfail = False
        self.debug = debug

    def start_update(self): 
        if self.debug: print("Update Started Device: " + self.name)
        self._can_update = True
        th.Thread(target=self._get_device_data, daemon=True).start()
    
    def stop_update(self):
        self._can_update = False

    def _get_device_data(self):
        while self._can_update:
            result = self.read_coils(4001)
            print(result)
            result = 11 if result else 00
            self.reg1 = result
            time.sleep(self.pollfreq)
            self._get_device_data()       
