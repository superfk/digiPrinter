import os, time, traceback
import win32api
import win32file
import win32process
import shutil

ROOT_PATH = os.path.join(os.environ["HOMEPATH"], "Desktop")
APP_FOLDER = os.path.join(ROOT_PATH, "digiPrint")
EXE_PATH =  os.path.join(APP_FOLDER, 'digiPrint.exe')
CONFIG_PATH =  os.path.join(APP_FOLDER, 'config.json')

def locate_usb():
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drname = '%c:\\' % chr(ord('A') + d)
            t = win32file.GetDriveType(drname)
            if t == win32file.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list


appLaunched = False
handle = None
usbInserted = False

while True:
    try:
        extUSBs = locate_usb()
        if len(extUSBs) > 0:
            if not usbInserted:
                usbInserted = True
                for eUsb in extUSBs:
                    external_ROOT_PATH = eUsb
                    external_EXE_PATH =  os.path.join(external_ROOT_PATH, 'digiPrint.exe')
                    external_CONFIG_PATH =  os.path.join(external_ROOT_PATH, 'config.json')
                    if os.path.exists(external_CONFIG_PATH):
                        shutil.copy(external_CONFIG_PATH,CONFIG_PATH)
                        print(f'Updated Config from {external_CONFIG_PATH}')
                    if os.path.exists(external_EXE_PATH) and appLaunched:
                        os.system("taskkill /f /im digiPrint.exe")
                        print(f'Terminated APP from {EXE_PATH}')
                        shutil.copy(external_EXE_PATH,EXE_PATH)
                        print(f'Updated APP from {external_EXE_PATH}')
                        appLaunched = False
                    elif os.path.exists(external_EXE_PATH) and not appLaunched:
                        shutil.copy(external_EXE_PATH,EXE_PATH)
                        print(f'Updated APP from {external_EXE_PATH}')
                        appLaunched = False
        else:
            usbInserted = False
            if not appLaunched:
                handle = win32process.CreateProcess(EXE_PATH,'', None , None , 0 ,win32process. CREATE_NEW_CONSOLE , None , None ,win32process.STARTUPINFO())
                print(f'Launched APP @ {EXE_PATH}')
                appLaunched = True
    except:
        errMsg = traceback.format_exc()
        print(errMsg)
    finally:
        time.sleep(1)

        