from time import sleep
from datetime import datetime

# import re
import pyvisa
import statistics

## connect to instrument
rm = pyvisa.ResourceManager()
# print(rm.list_resources())
baro = rm.open_resource('ASRLCOM8::INSTR',
                        baud_rate=9600,
                        read_termination='\n',
                        parity=pyvisa.constants.Parity.even,
                        data_bits=7
)

## Change these parameters before starting a measurement run
set_press = '1010 mbar'
note = 'Fall 2' # barometer at max range briefly before mmt
#note = 'Rise 2' # barometer at min range briefly before mmt

## create logging file and collect data for ~5 seconds
x = []
y = []
i = 1
with open('OPUS/raw_data.csv', 'a') as fp:
    fp.write('{}, {}'.format(set_press,note))
    fp.write('\n')
    while i < 6:
        mmt_read = baro.query('SEND')
        print(mmt_read)
        mmt_press = mmt_read.strip(' mbar\r')
        fp.write('{}, {}'.format(datetime.now(), mmt_press))
        fp.write('\n')
        x.append(i)
        y.append(float(mmt_press))
        sleep(1)
        i += 1
baro.close()

press_mean = sum(y)/len(y)
press_stdev = statistics.stdev(y)
print('Mean = ', press_mean)
print('Stdev = ',press_stdev)

with open('OPUS/summary_data.csv', 'a') as fs:
    fs.write('{}, {}, {}, {}, {}'.format(datetime.now(),set_press,note,press_mean,press_stdev))
    fs.write('\n')

with open('OPUS/raw_data.csv', 'a') as fp:
    fp.write('{}, {}, {}'.format({},press_mean,press_stdev))
    fp.write('\n')
    fp.write('\n')