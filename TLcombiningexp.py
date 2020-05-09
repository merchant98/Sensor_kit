

#!/usr/bin/python
from tkinter import *
import sys
import os
import time
import tkinter as tk 
import RPi.GPIO as GPIO
from tkinter import messagebox as mb
import csv
import Adafruit_DHT
import datetime
import tkinter.ttk as ttk
import spidev # To communicate with SPI devices
from time import sleep  # To add delay
import Adafruit_BMP.BMP085 as BMP085 #Pressure sensor
import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')


GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)  # touch s/w as an input pin 26  
root = Tk()
root.geometry("1000x1000")
root.configure(background='#ffffff')
root.title('Main Khidki')
name = ''
div = ''
roll = ''
exp = ''
#root.attributes('-type', 'dock') #Hide Title bar
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 
hum = 0.00
tem = 0.00
px_value = 0
py_value = 0
onetime = 0
delay = 3
#Button Functions
def ldr():
    global name
    global name1_file
    
    name1_file = name +'_ldr.csv'
    
    fieldnames = ["Time", "Light"]
    with open(name1_file, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    def analogInput(channel):
      spi.max_speed_hz = 1350000
      adc = spi.xfer2([1,(8+channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data
    # Below function will convert data to voltage
    def ldrupdate():
        global name1_file
        Time = '{:%d/%m/%y %H:%M:%S}'.format(datetime.datetime.now())
        temp_output = analogInput(1)/1023*100 #Channel Number
        temp_output = round(temp_output, 2)
        output_ldr.set("%d%%" %temp_output)
        print("%d" %temp_output)
        with open(name1_file, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                 
                    "Time": Time,
                    "Light": temp_output,
                    }
            csv_writer.writerow(info)
        global id1
        id1=winldr.after(3000,ldrupdate)

    def ldrpause():
        global id1
        print("Pause")
        winldr.after_cancel(id1)
        
    def ldrshow():
        global name1_file
        #pause()
        print("Pause and Show")
        tab = Toplevel()
        tab.title("Tkinter Table")
        tab.geometry("1024x768")

        TableMargin = Frame(tab, width=500)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("Time", "Light"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Time', text="Time", anchor=W)
        tree.heading('Light', text="Light", anchor=W)
        #tree.heading('Humidity', text="Humidity", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=200)
        tree.column('#2', stretch=NO, minwidth=0, width=200)
        #tree.column('#3', stretch=NO, minwidth=0, width=300)
        tree.pack()

        with open(name1_file) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Time = row['Time']
                Light = row['Light']
                #Humidity = row['Humidity']
                tree.insert("", 0, values=(Time, Light))

        #============================INITIALIZATION==============================
        if __name__ == '__main__':
            tab.mainloop()
            
    output_ldr = tk.StringVar()    
    winldr = Toplevel()
    winldr.geometry("500x500")
    winldr.configure(background='#CD5C5C')
    winldr.title('LDR Hai Apun') 
    label_1_ldr = Label(winldr, text='Light: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
    label_1_ldr.place(x=120, y=92)
    output_1_label_ldr = Label(winldr, textvariable=output_ldr, height=2, width=12)
    output_1_label_ldr.place(x=200, y=100)
    btn_ldrbegin=Button(winldr, text="Begin", command = ldrupdate)
    btn_ldrbegin.place(x=150, y=275)
    btn_ldrdestroy=Button(winldr, text="Quit", command = winldr.destroy)
    btn_ldrdestroy.place(x=250, y=275)
    btn_ldrshow=Button(winldr, text="Show", command = ldrshow)
    btn_ldrshow.place(x=150, y=325)
    btn_ldrpause=Button(winldr, text="Pause", command = ldrpause)
    btn_ldrpause.place(x=250, y=325)
    winldr.mainloop()
     



def dht():
    global name
    global name_file
    global x_value
    win = Toplevel()
    win.geometry("500x500")
    win.configure(background='#CD5C5C')
    win.title('DHT Hai Apun') 
    sensor = Adafruit_DHT.DHT11
    # connected to GPIO23.
    pin = 21
    x_value = '{:%d/%m/%y %H:%M:%S}'.format(datetime.datetime.now())
    total_1 = ''
    total_2 = ''
    #count = 0
    fieldnames = ["Time", "Temperature", "Humidity"]
    name_file = name +'dht.csv'
    with open(name_file, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    

    def show():
        global name_file
        pause()
        print("Pause and Show")
        tab = Toplevel()
        tab.title("Tkinter Table")
        tab.geometry("1024x768")

        TableMargin = Frame(tab, width=500)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("Time", "Temperature", "Humidity"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Time', text="Time", anchor=W)
        tree.heading('Temperature', text="Temperature", anchor=W)
        tree.heading('Humidity', text="Humidity", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=200)
        tree.column('#2', stretch=NO, minwidth=0, width=200)
        tree.column('#3', stretch=NO, minwidth=0, width=300)
        tree.pack()

        with open(name_file) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Time = row['Time']
                Temperature = row['Temperature']
                Humidity = row['Humidity']
                tree.insert("", 0, values=(Time, Temperature, Humidity))

        #============================INITIALIZATION==============================
        if __name__ == '__main__':
            tab.mainloop()
        
    
    def begin():
        global hum, tem
        global px_value
        global onetime
        global total_1
        global total_2
        global delay
        if onetime==0:
            px_value = int('{:%S}'.format(datetime.datetime.now())) + delay
            onetime+=1
        
        humidity, temperature = Adafruit_DHT.read(sensor, pin)
        if humidity is not None and temperature is not None:
           hum = humidity
           tem = temperature

        total_1 = tem
        total_2 = hum
        c_value = int('{:%S}'.format(datetime.datetime.now()))
            
        if px_value > 59:
            px_value=px_value-60
        if px_value == c_value:
            print(c_value)
            print(c_value+delay)
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(tem, hum))
            output_1.set("%d C" %tem)
            output_2.set("%d %%" %hum)
            px_value = int('{:%S}'.format(datetime.datetime.now())) + delay
            x_value = '{:%d/%m/%y %H:%M:%S}'.format(datetime.datetime.now())
            with open(name_file, 'a') as csv_file:
                 csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                 info = {"Time": x_value,"Temperature": total_1,"Humidity": total_2}
                 csv_writer.writerow(info)    
        global id
        id=win.after(1,begin)
    def pause():
        print("Pause")
        global id
        global onetime
        onetime = 0
        win.after_cancel(id)



    def graph():
        global name
        global name_file
        
        data = pd.read_csv(name_file)
        x = data['Time']
        y1 = data['Temperature']
        y2 = data['Humidity']
        d1 = {}
        tv = len(x)
        pl = int(tv/10)

        
        #
        plt.subplot(2,1,1)
        plt.cla()
        plt.plot(x, y1, label='Temperature', color ='red')
        plt.xlabel('Time(s)')
        plt.ylabel('Temp(C)')
        plt.legend(loc='lower right')
        plt.xticks(rotation = 90)
        #plt.text(d1, horizontalalignment='center',verticalalignment='bottom')
        plt.xticks(np.arange(0, tv, pl)) 

        plt.subplot(2,1,2)
        plt.cla()
        plt.plot(x, y2, label='Humidity', color='blue')
        plt.xlabel('Time(s)')
        plt.ylabel('Hum(%)')
        plt.legend(loc='lower right')
        plt.xticks(rotation = 90)
        #plt.text(d1, horizontalalignment='center',verticalalignment='bottom')
        plt.xticks(np.arange(0, tv, pl)) 

        #ani = FuncAnimation(plt.gcf(), animate, interval=10000)
        plt.tight_layout()
        plt.show()
  
        
    output_1 = tk.StringVar()
    output_2 = tk.StringVar()

    #Label Content
    label_1 = Label(win, text='Temp: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
    label_1.place(x=120, y=92)
    label_2 = Label(win, text='Humid: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
    label_2.place(x=120, y=192)

    #Label for Readings
    output_1_label = Label(win, textvariable=output_1, height=2, width=12)
    output_1_label.place(x=200, y=100)
    output_2_label = Label(win, textvariable=output_2, height=2, width=12)
    output_2_label.place(x=200, y=200)

    btn_x=Button(win, text="Begin", command = begin)
    btn_x.place(x=150, y=275)
    btn_p=Button(win, text="Pause", command = pause)
    btn_p.place(x=250, y=275)
    btn_s=Button(win, text="Show data", command = show)
    btn_s.place(x=250, y=325)
    btn_q=Button(win, text="Quit   ", command = win.destroy)
    btn_q.place(x=150, y=325)
    btn_pl=Button(win, text="Plot   ", command = graph)
    btn_pl.place(x=150, y=425)
    win.mainloop()

    
def touchsw():
        tout = ""
        #touch = GPIO.input(26) #read status
            #print(touch)
        
        def touchchk():
            touch = GPIO.input(20) 
            if touch==1:
                tout="ON"
                print("Switch On")
                output_1_label_tsw = Label(wintsw, text=tout, height=2, width=12)
                output_1_label_tsw.place(x=200, y=110)

            else:
                tout="OFF"
                output_1_label_tsw = Label(wintsw, text=tout, height=2, width=12)
                output_1_label_tsw.place(x=200, y=110)
                print("Switch Off")    
            wintsw.after(500,touchchk)
            
        tout = tk.StringVar()        
        wintsw = Toplevel()
        wintsw.geometry("500x300")
        wintsw.configure(background='#CD5C5C')
        wintsw.title('Preeti') 
        label_1_tsw = Label(wintsw, text="Switch:", font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
        label_1_tsw.place(x=120, y=100)
        #output_1_label_tsw = Label(wintsw, text=tout, height=2, width=12)
        #output_1_label_tsw.place(x=200, y=100)
        btn_ldrdestroy=Button(wintsw, text="Quit", command = wintsw.destroy)
        btn_ldrdestroy.place(x=230, y=225)
        btn_tswcheck=Button(wintsw, text="Check", command = touchchk)
        btn_tswcheck.place(x=225, y=175)
        wintsw.mainloop()


def atmp():
    global name
    global name_file4
    wap = Toplevel()
    wap.geometry("500x500")
    wap.configure(background='#CD5C5C')
    wap.title('Antariksh ka dabaav')
    fieldnames = ["Time", "Pressure", "Sea Pressure"]
    name_file4 = name +'atm.csv'
    with open(name_file4, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    #sensor = BMP085.BMP085()
    def atmup():
        sensor = BMP085.BMP085()
        pressure.set(sensor.read_pressure())
        seap.set(sensor.read_sealevel_pressure())
        print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
        print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
        pre = sensor.read_pressure()
        print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
        print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
        seapre = sensor.read_sealevel_pressure()
        x_value = '{:%d/%m/%y %H:%M:%S}'.format(datetime.datetime.now())
        with open(name_file4, 'a') as csv_file:
                 csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                 info = {"Time": x_value,"Pressure": pre,"Sea Pressure": seapre}
                 csv_writer.writerow(info)    
        global id
        id=wap.after(1000,atmup)

    def pause():
        print("Pause")
        global id
        wap.after_cancel(id)

    def show():
        global name_file4
        pause()
        print("Show")
        tab = Toplevel()
        tab.title("Tkinter Table")
        tab.geometry("1024x768")

        TableMargin = Frame(tab, width=500)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("Time", "Pressure", "Sea Pressure"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Time', text="Time", anchor=W)
        tree.heading('Pressure', text="Pressure", anchor=W)
        tree.heading('Sea Pressure', text="Sea Pressure", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=200)
        tree.column('#2', stretch=NO, minwidth=0, width=200)
        tree.column('#3', stretch=NO, minwidth=0, width=300)
        tree.pack()
        with open(name_file4) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Time = row['Time']
                Pressure = row['Pressure']
                Seap = row['Sea Pressure']
                tree.insert("", 0, values=(Time, Pressure, Seap))

        #============================INITIALIZATION==============================
        if __name__ == '__main__':
            tab.mainloop()
        



    
    pressure = tk.StringVar()
    seap = tk.StringVar()
     #Label Content
    label_1 = Label(wap, text='Pressure: ', font=("Helvetica", 15), height=2, width=11, bg='#CD5C5C')
    label_1.place(x=120, y=92)
    label_2 = Label(wap, text='Sea level Pressure: ', font=("Helvetica", 15), height=2, width=18, bg='#CD5C5C')
    label_2.place(x=45, y=192)

    #Label for Readings
    output_1_label = Label(wap, textvariable=pressure, height=2, width=15)
    output_1_label.place(x=300, y=100)
    output_2_label = Label(wap, textvariable=seap, height=2, width=15)
    output_2_label.place(x=300, y=200)

    btn_x=Button(wap, text="Begin", command = atmup)
    btn_x.place(x=150, y=275)
    btn_p=Button(wap, text="Pause", command = pause)
    btn_p.place(x=250, y=275)
    btn_s=Button(wap, text="Show data", command = show)
    btn_s.place(x=250, y=325)
    btn_q=Button(wap, text="Quit", command = wap.destroy)
    btn_q.place(x=150, y=325)
    wap.mainloop()
    


def lm35():
    global name
    global name_file5
    name_file5 = name +'_lm35.csv'
    
    fieldnames = ["Time", "Temperature"]
    with open(name_file5, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    def analogInput(channel):
      spi.max_speed_hz = 1350000
      adc = spi.xfer2([1,(8+channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data
    # Below function will convert data to voltage
    def lmupdate():
        global name_file5
        global output_temp
        Time = '{:%d/%m/%y %H:%M:%S}'.format(datetime.datetime.now())
        temp_output = analogInput(0) #Channel Number
        volts = (temp_output * 3.3) / 1024
        temperature = volts / (10.0 / 1000)
        temperature = round(temperature,2)
        output_lm.set("%d C" %temperature)
        print(temperature)
        
        #sleep(1)
        with open(name_file5, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                 
                    "Time": Time,
                    "Temperature": temperature,
                    }
            csv_writer.writerow(info)
        output_lm.set
        global id5
        id5=winlm.after(3000,lmupdate)

    def lmpause():
        global id5
        print("Pause")
        winlm.after_cancel(id5)
        
    def lmshow():
        global name1_file
        #pause()
        print("Pause and Show")
        tab = Toplevel()
        tab.title("Tkinter Table")
        tab.geometry("1024x768")

        TableMargin = Frame(tab, width=500)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("Time", "Temperature"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Time', text="Time", anchor=W)
        tree.heading('Temperature', text="Temperature", anchor=W)
        #tree.heading('Humidity', text="Humidity", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=200)
        tree.column('#2', stretch=NO, minwidth=0, width=200)
        #tree.column('#3', stretch=NO, minwidth=0, width=300)
        tree.pack()

        with open(name_file5) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                Time = row['Time']
                Temp = row['Temperature']
                #Humidity = row['Humidity']
                tree.insert("", 0, values=(Time, Temp))

        #============================INITIALIZATION==============================
        if __name__ == '__main__':
            tab.mainloop()
            
    output_lm = tk.StringVar()    
    winlm = Toplevel()
    winlm.geometry("500x500")
    winlm.configure(background='#CD5C5C')
    winlm.title('Lm35') 
    label_1_lm = Label(winlm, text='Temperature: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
    label_1_lm.place(x=120, y=92)
    output_1_label_lm = Label(winlm, textvariable=output_lm, height=2, width=12)
    output_1_label_lm.place(x=200, y=100)
    btn_lmbegin=Button(winlm, text="Begin", command = lmupdate)
    btn_lmbegin.place(x=150, y=275)
    btn_lmdestroy=Button(winlm, text="Quit", command = winlm.destroy)
    btn_lmdestroy.place(x=250, y=275)
    btn_lmshow=Button(winlm, text="Show", command = lmshow)
    btn_lmshow.place(x=150, y=325)
    btn_lmpause=Button(winlm, text="Pause", command = lmpause)
    btn_lmpause.place(x=250, y=325)
    winlm.mainloop()
     

def cap():

    def cloc():
        GPIO.setwarnings(False) # Ignore warning for now
        #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        
        pout = ""
            #touch = GPIO.input(26) #read status
                #print(touch)
            
        def proxchk():
            touch = GPIO.input(17) 
            if touch==1:
                pout="Nothing Nearby"
                print("Switch On")
                output_1_label_tsw = Label(winpro, text=pout, height=2, width=20)
                output_1_label_tsw.place(x=200, y=110)

            else:
                pout="Object detected"
                output_1_label_tsw = Label(winpro, text=pout, height=2, width=20)
                output_1_label_tsw.place(x=200, y=110)
                print("Switch Off")    
            winpro.after(500,proxchk)
                
        pout = tk.StringVar()        
        winpro = Toplevel()
        winpro.geometry("500x300")
        winpro.configure(background='#CD5C5C')
        winpro.title('Proximity') 
        label_1_tsw = Label(winpro, text="Status:", font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
        label_1_tsw.place(x=120, y=100)
            #output_1_label_tsw = Label(wintsw, text=tout, height=2, width=12)
            #output_1_label_tsw.place(x=200, y=100)
        btn_destroy=Button(winpro, text="Quit", command = winpro.destroy)
        btn_destroy.place(x=230, y=225)
        btn_check=Button(winpro, text="Check", command = proxchk)
        btn_check.place(x=225, y=175)
        winpro.mainloop()



    
    def rpm():
        GPIO.setwarnings(False) # Ignore warning for now
        #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        global name
        global name_file6
        name_file6 = name +'_RPM.csv'
        
        fieldnames = ["Time", "RPM"]
        with open(name_file6, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        global times
        global ptimes
        global interval
        global rpm
        times = 0
        ptimes = 0
        interval = 0
        rpm = 0 

        def rpmupdate():
            global times
            global ptimes
            global interval
            global rpm
        #while True: # Run forever
            print("Begin")
            while GPIO.input(17) == GPIO.LOW:
                global times
                #print("Utprerit")
                times=time.time()
                
            interval = times - ptimes
            if(interval):
                spd = 26.39 / interval / 100#cm/s to m/s
                rpm = (60*spd)/26.39 #m/s to speed (Depends on the diameter)
                rpm = rpm*100
                print(rpm)
                ptimes = times
                # Below function will convert data to voltage
            Time = '{:%d/%m/%y %H:%M:%S}'.format(datetime.datetime.now())
            output_rpm.set("%d" %rpm)
            #print(rpm)
            
            #sleep(1)
            with open(name_file6, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                info = {
                     
                        "Time": Time,
                        "RPM": rpm,
                        }
                csv_writer.writerow(info)
            global id6
            id6=winrpm.after(200,rpmupdate)

        def rpmpause():
            global id6
            print("Pause")
            winrpm.after_cancel(id6)
            
        def rpmshow():
            global name_file6
            #pause()
            print("Pause and Show")
            tab = Toplevel()
            tab.title("Tkinter Table")
            tab.geometry("1024x768")

            TableMargin = Frame(tab, width=500)
            TableMargin.pack(side=TOP)
            scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
            scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
            tree = ttk.Treeview(TableMargin, columns=("Time", "RPM"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
            scrollbary.config(command=tree.yview)
            scrollbary.pack(side=RIGHT, fill=Y)
            scrollbarx.config(command=tree.xview)
            scrollbarx.pack(side=BOTTOM, fill=X)
            tree.heading('Time', text="Time", anchor=W)
            tree.heading('RPM', text="RPM", anchor=W)
            #tree.heading('Humidity', text="Humidity", anchor=W)
            tree.column('#0', stretch=NO, minwidth=0, width=0)
            tree.column('#1', stretch=NO, minwidth=0, width=200)
            tree.column('#2', stretch=NO, minwidth=0, width=200)
            #tree.column('#3', stretch=NO, minwidth=0, width=300)
            tree.pack()

            with open(name_file6) as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    Time = row['Time']
                    Speed = row['RPM']
                    #Humidity = row['Humidity']
                    tree.insert("", 0, values=(Time, Speed))

            #============================INITIALIZATION==============================
            if __name__ == '__main__':
                tab.mainloop()
                
        output_rpm = tk.StringVar()    
        winrpm = Toplevel()
        winrpm.geometry("500x500")
        winrpm.configure(background='#CD5C5C')
        winrpm.title('Revving') 
        label_1_rpm = Label(winrpm, text='RPM: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
        label_1_rpm.place(x=120, y=92)
        output_1_label_rpm = Label(winrpm, textvariable=output_rpm, height=2, width=12)
        output_1_label_rpm.place(x=200, y=100)
        btn_rpmbegin=Button(winrpm, text="Begin", command = rpmupdate)
        btn_rpmbegin.place(x=150, y=275)
        btn_rpmdestroy=Button(winrpm, text="Quit", command = winrpm.destroy)
        btn_rpmdestroy.place(x=250, y=275)
        btn_rpmshow=Button(winrpm, text="Show", command = rpmshow)
        btn_rpmshow.place(x=150, y=325)
        btn_rpmpause=Button(winrpm, text="Pause", command = rpmpause)
        btn_rpmpause.place(x=250, y=325)
        winrpm.mainloop()


    winc = Toplevel()
    winc.geometry("500x200")
    winc.configure(background='#CD5C5C')
    winc.title('Choose exp') 
    #label_1_c = Label(winlm, text='Temperature: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
    #label_1_c.place(x=120, y=92)
    #output_1_label_c = Label(winlm, textvariable=output_lm, height=2, width=12)
    #output_1_label_c.place(x=200, y=100)
    btn_rpm=Button(winc, text="Check RPM", command = rpm)
    btn_rpm.place(x=150, y=75)
    btn_destroy=Button(winc, text="Quit", command = winc.destroy)
    btn_destroy.place(x=250, y=125)
    btn_lmshow=Button(winc, text="Proximity Alert", command = cloc)
    btn_lmshow.place(x=300, y=75)
    #btn_lmpause=Button(winc, text="Pause", command = lmpause)
    #btn_lmpause.place(x=250, y=325)
    winc.mainloop()


def ind():

    def clol():
        GPIO.setwarnings(False) # Ignore warning for now
        #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        
        pout = ""
            #touch = GPIO.input(26) #read status
                #print(touch)
            
        def proxchk():
            touch = GPIO.input(17) 
            if touch==1:
                pout="Nothing Nearby"
                print("Switch On")
                output_1_label_tsw = Label(winpro, text=pout, height=2, width=20)
                output_1_label_tsw.place(x=200, y=110)

            else:
                pout="Object detected"
                output_1_label_tsw = Label(winpro, text=pout, height=2, width=20)
                output_1_label_tsw.place(x=200, y=110)
                print("Switch Off")    
            winpro.after(500,proxchk)
                
        pout = tk.StringVar()        
        winpro = Toplevel()
        winpro.geometry("500x300")
        winpro.configure(background='#CD5C5C')
        winpro.title('Proximity') 
        label_1_tsw = Label(winpro, text="Status:", font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
        label_1_tsw.place(x=120, y=100)
            #output_1_label_tsw = Label(wintsw, text=tout, height=2, width=12)
            #output_1_label_tsw.place(x=200, y=100)
        btn_destroy=Button(winpro, text="Quit", command = winpro.destroy)
        btn_destroy.place(x=230, y=225)
        btn_check=Button(winpro, text="Check", command = proxchk)
        btn_check.place(x=225, y=175)
        winpro.mainloop()


    
    def rpml():
        GPIO.setwarnings(False) # Ignore warning for now
        #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        global name
        global name_file6
        name_file6 = name +'_RPML.csv'
        
        fieldnames = ["Time", "RPM"]
        with open(name_file6, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        global times
        global ptimes
        global interval
        global rpm
        times = 0
        ptimes = 0
        interval = 0
        rpm = 0 

        def rpmupdate():
            global times
            global ptimes
            global interval
            global rpm
        #while True: # Run forever
            print("Begin")
            while GPIO.input(17) == GPIO.LOW:
                global times
                #print("Utprerit")
                times=time.time()
                
            interval = times - ptimes
            if(interval):
                spd = 26.39 / interval / 100#cm/s to m/s
                rpm = (60*spd)/26.39 #m/s to speed (Depends on the diameter)
                rpm = rpm*100
                print(rpm)
                ptimes = times
                # Below function will convert data to voltage
            Time = '{:%d/%m/%y %H:%M:%S}'.format(datetime.datetime.now())
            output_rpm.set("%d" %rpm)
            #print(rpm)
            
            #sleep(1)
            with open(name_file6, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                info = {
                     
                        "Time": Time,
                        "RPM": rpm,
                        }
                csv_writer.writerow(info)
            global id6
            id6=winrpm.after(200,rpmupdate)

        def rpmpause():
            global id6
            print("Pause")
            winrpm.after_cancel(id6)
            
        def rpmshow():
            global name_file6
            #pause()
            print("Pause and Show")
            tab = Toplevel()
            tab.title("Tkinter Table")
            tab.geometry("1024x768")

            TableMargin = Frame(tab, width=500)
            TableMargin.pack(side=TOP)
            scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
            scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
            tree = ttk.Treeview(TableMargin, columns=("Time", "RPM"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
            scrollbary.config(command=tree.yview)
            scrollbary.pack(side=RIGHT, fill=Y)
            scrollbarx.config(command=tree.xview)
            scrollbarx.pack(side=BOTTOM, fill=X)
            tree.heading('Time', text="Time", anchor=W)
            tree.heading('RPM', text="RPM", anchor=W)
            #tree.heading('Humidity', text="Humidity", anchor=W)
            tree.column('#0', stretch=NO, minwidth=0, width=0)
            tree.column('#1', stretch=NO, minwidth=0, width=200)
            tree.column('#2', stretch=NO, minwidth=0, width=200)
            #tree.column('#3', stretch=NO, minwidth=0, width=300)
            tree.pack()

            with open(name_file6) as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    Time = row['Time']
                    Speed = row['RPM']
                    #Humidity = row['Humidity']
                    tree.insert("", 0, values=(Time, Speed))

            #============================INITIALIZATION==============================
            if __name__ == '__main__':
                tab.mainloop()
                
        output_rpm = tk.StringVar()    
        winrpm = Toplevel()
        winrpm.geometry("500x500")
        winrpm.configure(background='#CD5C5C')
        winrpm.title('Revving') 
        label_1_rpm = Label(winrpm, text='RPM: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
        label_1_rpm.place(x=120, y=92)
        output_1_label_rpm = Label(winrpm, textvariable=output_rpm, height=2, width=12)
        output_1_label_rpm.place(x=200, y=100)
        btn_rpmbegin=Button(winrpm, text="Begin", command = rpmupdate)
        btn_rpmbegin.place(x=150, y=275)
        btn_rpmdestroy=Button(winrpm, text="Quit", command = winrpm.destroy)
        btn_rpmdestroy.place(x=250, y=275)
        btn_rpmshow=Button(winrpm, text="Show", command = rpmshow)
        btn_rpmshow.place(x=150, y=325)
        btn_rpmpause=Button(winrpm, text="Pause", command = rpmpause)
        btn_rpmpause.place(x=250, y=325)
        winrpm.mainloop()
    winl = Toplevel()
    winl.geometry("500x200")
    winl.configure(background='#CD5C5C')
    winl.title('Choose exp') 
    #label_1_c = Label(winlm, text='Temperature: ', font=("Helvetica", 15), height=2, width=6, bg='#CD5C5C')
    #label_1_c.place(x=120, y=92)
    #output_1_label_c = Label(winlm, textvariable=output_lm, height=2, width=12)
    #output_1_label_c.place(x=200, y=100)
    btn_rpm=Button(winl, text="Check RPM", command = rpml)
    btn_rpm.place(x=150, y=75)
    btn_destroy=Button(winl, text="Quit", command = winl.destroy)
    btn_destroy.place(x=250, y=125)
    btn_show=Button(winl, text="Proximity Alert", command = clol)
    btn_show.place(x=300, y=75)
    #btn_lmpause=Button(winc, text="Pause", command = lmpause)
    #btn_lmpause.place(x=250, y=325)
    winl.mainloop()



        

#Button Functions
def form():
    global read
    form = tk.Tk()
    form.geometry("500x500")
    form.configure(background='#ffeded')
    form.title('Aadhar Form')
    open1 = open("API.txt", "r") #opens file to read it
    read = open1.read()
    open1.close()
    print(read)
    output_API_label = Label(form, text ='API:' + read, height=2, width=15)
    output_API_label.place(x=200, y=10)
    def clear():
       entry_1.delete(0, END)
       entry_2.delete(0, END)
       entry_3.delete(0, END)
       entry_1.focus_set()

    def update_api():
        uapi = Toplevel()
        uapi.geometry("400x200")
        uapi.configure(background='#ffeded')
        uapi.title('Internet Kendra')
        def readuapi():
            global read
            name = open("API.txt", "w") #opens file usernames.txt and gets ready to write to it
            file = en_1.get()
            name.write(file) #writes contents in file to usernames.txt
            name.close() #closes file
            open1 = open("API.txt", "r") #opens file to read it
            read = open1.read()
            open1.close()
            output_API_label = Label(form, text ='API:' + read, height=2, width=15)
            output_API_label.place(x=200, y=10)
            uapi.destroy()    
        la_1 = Label(uapi, text='  API ', anchor='w',  font=("Helvetica", 10), height=2, width=38, bg='#f66262')
        la_1.place(x=60, y=60)
        en_1 = Entry(uapi)
        en_1.place(x=175,y=66)
        b3=Button(uapi, text="Quit", command = uapi.destroy,height = 1, width = 8)
        b3.place(x=50, y=100)
        b1=Button(uapi, text="Submit", command = readuapi,height = 1, width = 8)
        b1.place(x=200, y=100)
        uapi.mainloop()

    def submit():
       global name
       global roll
       global div
       global exp
       global name_file
       if entry_1.get() == "" or entry_2.get() == "" or entry_3.get() == "":
          mb.showerror("Error","Please Input All Data",parent=form)
          print("Khali Hai")
       else:
           name = entry_1.get()
           print(name)
           roll = int(entry_2.get())
           print(roll)
           div = entry_3.get()
           print(div)
           #print(exp.get())
           mb.showinfo("Data","Name: " + name +"\n" + "Roll Number: " + entry_2.get() +"\n" + "Division: " + div +"\n" + "API: " + read,parent=form)
           #Label on main screen
           info_n = Label(root, text = name, height=2, width=40, wraplength=1000)
           info_n.place(x=500, y=50)
           info_r = Label(root, text = roll, height=2, width=40, wraplength=1000)
           info_r.place(x=500, y=100)
           info_d = Label(root, text = div, height=2, width=40, wraplength=1000)
           info_d.place(x=500, y=150)
           form.destroy()

    #label and Entry box
    label_1 = Label(form, text='  Name ', anchor='w',  font=("Helvetica", 10), height=2, width=38, bg='#f66262')
    label_1.place(x=60, y=60)
    entry_1 = Entry(form)
    entry_1.place(x=175,y=66)
    label_2 = Label(form, text='  Roll No ', anchor='w',  font=("Helvetica", 10), height=2, width=38, bg='#f66262')
    label_2.place(x=60, y=120)
    entry_2 = Entry(form)
    entry_2.place(x=175,y=126)
    label_3 = Label(form, text='  Class/Division ', anchor='w',  font=("Helvetica", 10), height=2, width=38, bg='#f66262')
    label_3.place(x=60, y=180)
    entry_3 = Entry(form)
    entry_3.place(x=175,y=186)
    #buttons
    b1=Button(form, text="Submit", command = submit,height = 1, width = 8)
    b1.place(x=100, y=275)
    b2=Button(form, text="Reset", command = clear,height = 1, width = 8)
    b2.place(x=250, y=275)
    b3=Button(form, text="Quit", command = form.destroy,height = 1, width = 8)
    b3.place(x=250, y=325)
    b4=Button(form, text="Update API", command = update_api,height = 1, width = 8)
    b4.place(x=100, y=325)
    form.mainloop()


#Abvolt Logo Code
photo = PhotoImage(file="Abvolt.gif")
label = Label(image=photo)
label.image = photo # keep a reference!
label.place(x=175, y=50)

#Experiment Buttons
E1=tk.Button(text="Experiment No. 1: \nDHT11", command = dht)
E1.place(x=100, y=200)

E2=tk.Button(text="Experiment No. 2: \nLDR", command = ldr)
E2.place(x=300, y=200)

E3=tk.Button(text="Experiment No. 3: \nTouch Switch", command = touchsw)
E3.place(x=100, y=300)

E4=tk.Button(text="Experiment No. 4: \nAtm. Pressure", command = atmp)
E4.place(x=300, y=300)

E5=tk.Button(text="Experiment No. 5: \nLM35", command = lm35)
E5.place(x=100, y=400)

E6=tk.Button(text="Experiment No. 6: \nCapacitive(C)", command = cap)
E6.place(x=300, y=400)

E7=tk.Button(text="Experiment No. 7: \nInducitve", command = ind)
E7.place(x=100, y=500)

#E8=tk.Button(text="Experiment No. 8: \nProx.(C)", command = cloc)
#E8.place(x=300, y=500)

#E9=tk.Button(text="Experiment No. 9: \nProx.(L)", command = clol)
#E9.place(x=100, y=600)

F=tk.Button(text="Enter Details", command = form)
F.place(x=215, y=150)


root.mainloop()
 
