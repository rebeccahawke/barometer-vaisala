### This is a short script to read data from a Vaisala barometer PTB330

from datetime import datetime
import statistics
import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())

# connect to instrument
baro = pyvisa.ResourceManager().open_resource('ASRLCOM8::INSTR',
                        baud_rate=4800,
                        read_termination='>',
                        parity=pyvisa.constants.Parity.even,
                        data_bits=7
)

baro.write('ECHO OFF')
baro.write('FORM 4.3 P " " U \RN')

baro.write('R')

#with open('Datalogging/summary_data.csv', 'a') as fs:
#    fs.write('{},{},{},{},{}'.format('Timestamp', 'Pressure', 'Pressure stdev', 'Temperature', 'Temperature stdev'))
#    fs.write('\n')

collectdata = True
while collectdata == True:
    i = 0
    press = []
    #with open('Datalogging/raw_data.csv', 'a') as fp:
    while i < 10:
            bytes = baro.get_visa_attribute(1073676460)
            if bytes > 11:
                data = baro.read_bytes(bytes).decode("utf-8")
                print(data)
                mmt_press = data.strip(' hPa')
                #print('Pressure (hPa) = ', mmt_press)
                press.append(float(mmt_press))
               #fp.write('{}, {}, {}'.format(datetime.now(), mmt_press, mmt_temp))
               # fp.write('\n')
                i += 1

    press_mean = sum(press)/len(press)
    press_stdev = statistics.stdev(press)
    print('Mean Pressure = ', press_mean)
    print('Stdev of Pressure = ',press_stdev)


    with open('Datalogging/summary_data.csv', 'a') as fs:
        fs.write('{},{},{}'.format(datetime.now(),press_mean,press_stdev))
        fs.write('\n')

    collectdata = False

baro.write('S')
baro.close()