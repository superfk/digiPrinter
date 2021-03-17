from escpos.printer import Network
import datetime,time
from corelib.hardwarelib.digitest import GelomatDigitest
from config import cfg
import keyboard
import statistics
import traceback

class PrinterAPI():
    def __init__(self) -> None:
        self.ip = '192.168.192.168'
        self.p = None
        self.connected = False
    
    def config(self):
        try:
            self.ip = cfg.getValue('ip')
        except:
            self.ip = '192.168.192.168'
    
    def connect(self):
        try:
            self.p.close()
            self.p = None
        except:
            pass
        finally:
            self.config()
            try:
                self.p = Network(self.ip,timeout=1)
                self.connected = True
                return self.connected
            except:
                self.connected = False
                print("Printer connecting error")
    
    def printText(self, text=''):
        try:
            self.p.text(f"{text}\n")
        except:
            self.connected = False
            print("Printer printing error")

    def cut(self):
        try:
            self.p.cut()
        except:
            self.connected = False
            print("Printer cutting error")
    
    def testPage(self):
        try:
            tfmt = cfg.getValue('time_format')
            curTime = datetime.datetime.now().strftime(tfmt)
            self.printText(f'''
            [This is Test Page]\n
            \n
            printing date: {curTime}
            \n\n\n\n
            [This is End of Test Page]
            ''')
            self.cut()
        except:
            self.connected = False
            print("Printer printing test page error")


class MainAPI():
    def __init__(self) -> None:
        self.version = '1.0.0'
        self.gelomat = GelomatDigitest()
        self.printer = PrinterAPI()
        self.dataset = []
        self.batchStart = True
        self.batchMearing = False
        self.batchEnd = False
        self.com = cfg.getValue('com')
        self.ip = cfg.getValue('ip')
        self.tfmt = cfg.getValue('time_format')
        self.errMsg = None
        self.gelomat_error = False
        self.usbInserted = False
    
    def getTime(self, getRaw=False):
        t = datetime.datetime.now()
        if getRaw:
            return t
        return t.strftime(self.tfmt)

    def waitMear(self):
        statusCode, value = self.gelomat.get_single_value()
        return value, statusCode
    
    def initHW(self):
        if not self.printer.connected:
            self.printer.connect()

        if not self.gelomat.connected:
            try:
                self.gelomat.close()
            except:
                pass
            finally:
                try:
                    self.com = cfg.getValue('com')
                    self.gelomat.open(self.com, timeout=1)
                    self.gelomat.config(debug=False, wait_cmd = False)
                    self.gelomat_error = False
                except:
                    self.gelomat.connected = False
                    if not self.gelomat_error:
                        errMsg = "Error occured: Gelomat connection error"
                        print(f"{errMsg}")
                        self.gelomat_error = True
                        if self.printer.connected:
                            self.printer.printText(f"{errMsg}\n")


    def printHeader(self):
        devName = self.gelomat.get_dev_name()
        lift = self.gelomat.get_lift()
        mode = self.gelomat.get_mode()
        self.printer.printText(f"[Configuration]\n")
        self.printer.printText(f"Program ver.: {self.version}\n")
        self.printer.printText(f"COM: {self.com}\n")
        self.printer.printText(f"Printer IP: {self.ip}\n")
        self.printer.printText(f"Device name: {devName}\n")
        self.printer.printText(f"Lift: {lift} mm\n")
        self.printer.printText(f"Mode: {mode}\n\n")

    def printBody(self):
        value, statusCode = self.waitMear()
        mearT = self.getTime()
        if statusCode == 1:
            if len(self.dataset) == 0:
                self.printer.printText(f"[Measurement Start] @ {mearT}\n")
            self.printer.printText(f"{mearT}\t{value}\n")
            self.dataset.append(value)
        elif statusCode < 0:
            if len(self.dataset) == 0:
                self.printer.printText(f"[Measurement Start] @ {mearT}\n")
            self.printer.printText(f"{mearT}\tdistance too big when measuring\n")
        else:
            return 0

    def printFooter(self):
        mearT = self.getTime()
        self.printer.printText(f"[Measurement End] @ {mearT}\n\n")             
        self.printer.printText(f"[Summary]\n")
        self.printer.printText(f"number of measurements: {len(self.dataset)}\n")
        avg = 0.0
        median = 0.0
        stdev = 0.0
        maxV = 0.0
        minV = 0.0
        if len(self.dataset) == 0:
            pass
        elif len(self.dataset) == 1:
            avg = self.dataset[0]
            median = self.dataset[0]
            maxV = self.dataset[0]
            minV = self.dataset[0]
        else:
            avg = round(statistics.mean(self.dataset), 1)
            median = round(statistics.median(self.dataset), 1)
            stdev = round(statistics.stdev(self.dataset), 1)
            maxV = round(max(self.dataset), 1)
            minV = round(min(self.dataset), 1)

        self.printer.printText(f"mean: {avg}\n")
        self.printer.printText(f"median: {median}\n")
        self.printer.printText(f"stdev: {stdev}\n")
        self.printer.printText(f"max: {maxV}\n")
        self.printer.printText(f"min: {minV}\n")
        self.printer.cut()
        self.dataset = []

    def printConfig(self):
        # "ip":"192.168.192.168",
        # "com": "COM3",
        # "time_format": "%Y-%m-%d %H:%M:%S",
        # "decimal": 1,
        # "key_batchend": "enter",
        # "key_cut": "7",
        # "key_testpage": "9",
        # "key_clearError": "0"
        try:
            com = cfg.getValue('com')
            ip = cfg.getValue('ip')
            time_format = cfg.getValue('time_format')
            key_batchend = cfg.getValue('key_batchend')
            key_cut = cfg.getValue('key_cut')
            key_testpage = cfg.getValue('key_testpage')
            key_clearError = cfg.getValue('key_clearError')
            self.printer.printText(f"COM: {com}\n")
            self.printer.printText(f"Printer IP: {ip}\n")
            self.printer.printText(f"Time Format: {time_format}\n")
            self.printer.printText(f"Key of Batch End: {key_batchend}\n")
            self.printer.printText(f"Key of Cut Page: {key_cut}\n")
            self.printer.printText(f"Key of Print Test Page: {key_testpage}\n")
            self.printer.printText(f"Key of Print Config: {5}\n")
            self.printer.printText(f"Key of Clear Error: {key_clearError}\n")
        except:
            print("Printer printing config page error")
    
    def main(self):
        startT = time.time()
        tString = self.getTime()
        print(f'[Program Start] @ {tString}')
        print(f'[Program Version] @ {self.version}')
        print('')
        while True:
            try:
                self.initHW()
                # all instr are connected, waitiing for data
                if keyboard.is_pressed(cfg.getValue('key_batchend')):
                    self.batchEnd = True
                if keyboard.is_pressed(cfg.getValue('key_clearError')):
                    self.errMsg = None
                if keyboard.is_pressed(cfg.getValue('key_cut')):
                    self.printer.cut()
                if keyboard.is_pressed(cfg.getValue('key_testpage')):
                    self.printer.testPage()
                if keyboard.is_pressed('5'):
                    self.printConfig()

                if self.gelomat.connected and self.printer.connected:
                    if self.batchStart:
                        self.printHeader()
                        self.batchStart = False
                        self.batchMearing = True
                        self.batchEnd = False
                    
                    if self.batchMearing:
                        self.printBody()

                    if self.batchEnd:
                        if self.batchMearing:
                            self.printFooter()
                            self.batchStart = True
                        self.batchEnd = False
                self.errMsg = None
            except:
                if self.errMsg is None:
                    self.errMsg = traceback.format_exc()
                    errMsg = f"Error occured: {self.errMsg}"
                    print(f"{errMsg}")
                    if self.printer.connected:
                        self.printer.printText(f"{errMsg}\n")
            finally:
                curT = time.time()
                curTString = self.getTime()
                if (curT - startT) >= 30:
                    print(f'[Program is still alive] @ {curTString}')
                    startT = curT
                time.sleep(0.2)


if __name__=='__main__':
    app = MainAPI()
    app.main()