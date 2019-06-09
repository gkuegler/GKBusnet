import device_library as devlib

mode_debug = False

dev = list()

# Initialize These Devices
dev.append(devlib.Device(name='pH Meter', host='127.0.0.1', port=62500, reg1='pH', debug=mode_debug))
dev[0].reg1 = 7.00
dev.append(devlib.Device(name='Temp Probe', host='127.0.0.1', port=62300, reg1='temp degF', debug=mode_debug))
dev[1]._testfail=True

def start_all_device_data():
    for i,x in enumerate(dev):
        dev[i].start_update()

if __name__ == '__main__':

    def listdevices():
        for i, x in enumerate(dev):
            print(str(i) + ':  ' + dev[i].name + ' | Com-Type: ' + dev[i].comprotocol + str(dev[i].host()))
            print('    Registers:')
            print('       Reg1: {} Type: {}'.format(dev[i].reg1, dev[i].reg1_type))
            #NEED TO ADD REGISTERS INITED AND DESCRIPTIONS OF THE REGISTERS

    print('Devices Loaded:')
    listdevices()

    print(dev[0].cerror)