import serial
from threading import Thread, Timer
from time import sleep


class SerialRead(Thread):
    work = True

    func = None

    def __init__(self, com_num, app):
        super().__init__()
        self.app = app
        self.daemon = True
        try:
            print(com_num)
            self.ser = serial.Serial('COM' + str(com_num), 115200)

            self.ser.timeout = 0.01
        except:
            self.work = False

    def run(self):
        while self.work:
            if self.ser.is_open:
                try:
                    s = self.ser.readline().decode('utf-8').strip()
                    self.func(self.app, s)
                    self.ser.flushInput()
                    self.ser.flushOutput()
                except:
                    pass
            sleep(0.025)

    def close_serial(self):
        if hasattr(self, 'ser'):
            self.ser.close()

    def conn_lost(self):
        self.app.setConnectionStatus(0)

    def conn_restored(self):
        self.app.setConnectionStatus(1)
