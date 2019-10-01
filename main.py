from ctypes import windll
import os

from tkinter import *
from PIL import Image, ImageTk

from ser import SerialRead

from temp_address import temp_address

user32 = windll.user32
user32.SetProcessDPIAware()

appdata_path = os.getenv('APPDATA') + '\\TempSensor\\'
if not os.path.exists(appdata_path):
    os.makedirs(appdata_path)

class TempSensorApp:
    com_num = 5

    TEMP_COUNT = 26

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.master.title("Temperature Sensor")
        self.master.iconbitmap("icon2.ico")

        self.height = 700
        self.width = 400
        self.x = 100
        self.y = 100

        self.load_params()

        self.frame.title = 'TemperatureSensor'
        self.master.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.master.resizable(True, True)
        self.master.bind('<Configure>', self.on_resize)


        self.setupUI()

        self.connect()

    def save_params(self):
        try:
            f = open(appdata_path + 'settings.txt', 'w')
            f.write(str(self.com_num)+'\n')
            f.write(str(self.master.winfo_height()) + '\n')
            f.write(str(self.master.winfo_width()) + '\n')
            f.write(str(self.master.winfo_x()) + '\n')
            f.write(str(self.master.winfo_y()) + '\n')
            f.close()
        except:
            print('save params error')

    def load_params(self):
        try:
            f = open(appdata_path + 'settings.txt')
            self.com_num = int(f.readline())
            self.height = int(f.readline())
            self.width = int(f.readline())
            self.x = int(f.readline())
            self.y = int(f.readline())
            f.close()
        except:
            print('load params error')

    def setupUI(self):
        self.com_label = Label(text='COM', font=("Courier", 11))
        self.com_label.place(x=10, y=6)

        self.com_text = StringVar()
        self.com_entry = Entry(textvariable=self.com_text, font=("Courier", 11))
        self.com_entry.place(x=50, y=7, width=30)
        self.com_text.set(str(self.com_num))

        self.conn_button = Button(text='Connect', font=("Calibri", 9), width=10)
        self.conn_button.bind('<ButtonRelease-1>', lambda event: self.connect())
        self.conn_button.place(x=90, y=2)

        self.conn_label = Label(text='Connection:', font=("Courier", 11), width=130)
        self.conn_label.place(x=200, y=5, width=180)

        self.canvas = Canvas(self.conn_label, width=50, height=20)
        self.canvas.place(x=148, y=0)

        # self.speed_label = Label(text='Speed: None', font=("Courier", 26))
        # self.speed_label.place(relx=0.05, y=60, relwidth=0.9)

        self.bg = Image.open('img/background.jpg')
        bg = self.bg.resize((700, 350))
        bg_tk = ImageTk.PhotoImage(bg)
        self.bg_image = Label(self.master, image=bg_tk, text="aaa")
        self.bg_image.image = bg_tk
        self.bg_image.place(relwidth=1, relheight=.9, rely=.1, x=0)

        self.temp_vars = [StringVar() for i in range(self.TEMP_COUNT)]
        for var in self.temp_vars:
            var.set('0.0')
        self.temp_labels = [Label(textvariable=var, bg='#727272', font=("Arial", 14)) for var in self.temp_vars]
        self.temp_labels[0].place(relx=.08, rely=.37)
        self.temp_labels[1].place(relx=.08, rely=.5)
        self.temp_labels[2].place(relx=.21, rely=.43)
        self.temp_labels[3].place(relx=.21, rely=.57)
        self.temp_labels[4].place(relx=.34, rely=.49)
        self.temp_labels[5].place(relx=.34, rely=.63)
        self.temp_labels[6].place(relx=.465, rely=.55)
        self.temp_labels[7].place(relx=.465, rely=.69)
        self.temp_labels[8].place(relx=.59, rely=.61)
        self.temp_labels[9].place(relx=.59, rely=.75)
        self.temp_labels[10].place(relx=.72, rely=.67)
        self.temp_labels[11].place(relx=.72, rely=.81)
        self.temp_labels[12].place(relx=.87, rely=.68)
        self.temp_labels[13].place(relx=.87, rely=.81)
        self.temp_labels[14].place(relx=.925, rely=.58)
        self.temp_labels[15].place(relx=.925, rely=.73)
        self.temp_labels[16].place(relx=.88, rely=.50)
        self.temp_labels[17].place(relx=.83, rely=.38)
        self.temp_labels[18].place(relx=.74, rely=.52)
        self.temp_labels[19].place(relx=.56, rely=.43)
        self.temp_labels[20].place(relx=.42, rely=.37)
        self.temp_labels[21].place(relx=.34, rely=.24)
        self.temp_labels[22].place(relx=.34, rely=.37)
        self.temp_labels[23].place(relx=.25, rely=.19)
        self.temp_labels[24].place(relx=.25, rely=.33)
        self.temp_vars[25].set('Отсек: 0.0')
        self.temp_labels[25].place(relx=.95, rely=.15, anchor=E)


    def on_resize(self, event):
        self.save_params()
        img = ImageTk.PhotoImage(self.bg.resize((self.master.winfo_width(), int(self.master.winfo_height()*.9))))
        self.bg_image.configure(image=img)
        self.bg_image.image = img

    def on_get_data(self, s):
        values = s.split(';')
        address = values[1].split(':')[1]
        index = temp_address.get(address)
        temp = values[2].split(':')[1]
        self.temp_vars[index].set(temp)

    def connect(self):
        self.com_num = int(self.com_text.get())
        self.save_params()
        if hasattr(self, 'reader'):
            self.reader.close_serial()
        self.reader = SerialRead(self.com_num, self)
        self.reader.func = self.on_get_data
        self.reader.start()

    def setConnectionStatus(self, status):
        if status == 1:
            color = 'green'
        else:
            color = 'red'
        self.canvas.create_oval(2, 3, 18, 19, fill=color)

    def setSpeed(self, value):
        between_sensors = 63 / 1000
        time = value / 1000
        speed = between_sensors / time
        try:
            speed1 = str(speed)[:str(speed).find('.')+3]
        except:
            speed1 = str(speed)
        self.speed_label['text'] = 'Speed: ' + speed1 + 'm/s'

    def setCOMport(self, value):
        self.com_label['text'] = 'COM' + str(value)

if __name__ == '__main__':
    root = Tk()
    app = TempSensorApp(root)
    root.mainloop()
