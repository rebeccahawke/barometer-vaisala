from time import sleep
from datetime import datetime

import re
import pyvisa

# connect to instrument
rm = pyvisa.ResourceManager()
print(rm.list_resources())
# TODO: get user to select correct resource from list?

baro = rm.open_resource('ASRLCOM8::INSTR',
                        baud_rate=9600,
                        read_termination='>',
                        parity=pyvisa.constants.Parity.even,
                        data_bits=7
)

# get serial number of instrument
dev_info = baro.query('?')
s = re.search(r'Serial number\s+:\s+(\w+)', dev_info)
sn = s.group(1)
print(sn)
# TODO: can link other info from ? query as needed - use online tool at https://regex101.com/

# set format of output
baro.query('FORM 4.3 P " " U \T 2.3 TP1 " " U \RN')
# TODO: change these query commands to writes when happy with script

# collect data for current time (once) and identify relevant data within
mmt_read = baro.query('SEND')
print(mmt_read)
mmt_press = re.search(r'(\d\d\d\d.\d\d\d)', mmt_read).group(1)
mmt_temp = re.search(r'\s+(\d\d.\d\d\d)', mmt_read).group(1)
print('Pressure (hPa) =', mmt_press)
print('Temperature (\xb0C) =', mmt_temp)

# create logging file and collect data for 5 seconds
x = []
y = []
i = 1
with open('PT.csv', 'w') as fp:
    while i < 6:
        mmt_read = baro.query('SEND')
        print(mmt_read)
        fp.write('{}, {}, {}'.format(datetime.now(), mmt_press, mmt_temp))
        fp.write('\n')
        x.append(i)
        y.append(float(mmt_press))
        sleep(1)
        i += 1

print(x)
print(y)



baro.close()