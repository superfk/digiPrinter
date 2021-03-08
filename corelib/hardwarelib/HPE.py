import sys, os
import time
import re
import matplotlib.pyplot as plt

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
DB_DIR = SCRIPT_DIR
indentLevel = 2
for i in range(indentLevel):
    DB_DIR = os.path.split(DB_DIR)[0]
sys.path.append(os.path.normpath(os.path.join(PACKAGE_PARENT,SCRIPT_DIR)))
sys.path.append(os.path.normpath(DB_DIR))

from corelib.hardwarelib.digitest import Digitest

class HPE3(Digitest):
    def __init__(self):
        super().__init__()
    def get_sn(self):
        return self.write_and_read('GET', 'DEV_SN')  
    def get_send_format(self):
        return self.write_and_read('GET', 'DEV_SEND_FORMAT')
    def get_all_data(self):
        self.write_and_read('GET', 'DATA=SEND_ALL', value=None)
        datalist = self.device.readlines()
        datalist_values = [float(x.decode()) for x in datalist] 
        return datalist_values  
    def get_single_value(self):
        while True:
            try:
                data = self.device.readline()
                data = data.decode()
                if data == '':
                    return 0, None
                return 1, float(data)
            except:
                return -1, None
    
    def erase_all_data(self):
        self.write_and_read('SET', 'DATA=ERASE_ALL')  
    def erase_last_data(self):
        self.write_and_read('SET', 'DATA=ERASE_LAST')  
            

if __name__ == '__main__':
    # test_rotation_single_mear()
    # test_rotation_graph_mear()
    ba = HPE3HPE()
    ba.open("COM3")
    ba.config(debug=False)
    ret = ba.get_dev_name()
    print(ret)
    ret = ba.get_dev_software_version()
    print(ret)
    ret = ba.get_sn()
    print(ret)
    ret = ba.get_ms_duration()
    print(ret)
    ret = ba.get_ms_method()
    print(ret)
    ret = ba.get_send_format()
    print(ret)
    ret = ba.get_all_data()
    print(ret)
    ret = ba.erase_all_data()
    print(ret)
    ret = ba.get_all_data()
    print(ret)
    ret = ba.set_ms_duration(5)
    print(ret)
    # ret = ba.write_and_read('GET','SYSTEM', value=None)
    # ret = ba.write_and_read('GET','DATA=SEND_ALL', value=None)
    # print(ret)
    while True:
        ret = ba.get_single_value()
        print(ret)
        if ret[0] == 1:
            break
    
    ret = ba.erase_last_data()
    print(ret)
    ret = ba.get_all_data()
    print(ret)

    ba.close()