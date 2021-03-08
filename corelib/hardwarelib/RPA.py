import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
DB_DIR = SCRIPT_DIR
indentLevel = 2
for i in range(indentLevel):
    DB_DIR = os.path.split(DB_DIR)[0]
sys.path.append(os.path.normpath(os.path.join(PACKAGE_PARENT,SCRIPT_DIR)))
sys.path.append(os.path.normpath(DB_DIR))

import threading
import time
import socket


class RPA(object):
    def __init__(self):
        self.sock = None
        self.connected = False

    def check_connection(self, addr, port=80):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.sock = s
            try:
                self.sock.settimeout(0.5)
                self.sock.connect((addr, port))
                self.sock.close()
                return True
            except (OSError,ConnectionRefusedError):
                self.sock.close()
                return False

    def open(self, addr, port=80):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.sock = s
            try:
                self.sock.settimeout(0.5)
                self.sock.connect((addr, port))
                self.connected = True
                return True
            except (OSError,ConnectionRefusedError):
                s.close()
                return False

    def close(self):
        self.sock.close()
        self.connected = False

if __name__ == '__main__':
    ret = RPA().check_connection('localhost', 80)
    print('connect status {}'.format(ret))