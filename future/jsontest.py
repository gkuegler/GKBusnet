import json

class Device():
    def __init__(self, name, host, port, reg1, reg2):
        self.name = name
dev = []
data = {}

data['devices'] = []

data['devices'].append({
    'name': 'pH PLC',
    'host': '127.0.0.1',
    'port': '62500',
    'reg1': 'pH',
    'reg2': 'status'
    })

data['devices'].append({
    'name': 'Temp Probe',
    'host': '127.0.0.1',
    'port': '62600',
    'reg1': 'Temp degF',
    'reg2': 'status'
    })

with open('data.txt', 'w') as file:  
    json.dump(data, file)

with open('data.txt', 'r') as file:  
    load = json.load(file)
    for i,x in enumerate(load['devices']):
        dev.append(Device(name=x['name'], host=x['host'],
            port=x['port'], reg1=x['reg1'], reg2=x['reg2']))

print(dev[0].name)
        