import tkinter as tk
import RPi.GPIO as GPIO
from tkinter import *
from time import strftime
import max6675
from bpg400.bpg400 import BGP400_RS232
from labdevices.pressuregauge import PressureGaugeUnit
from PIL import Image, ImageTk

#relay board pin setup
inPM=3
inPD=5
inPWC=7
inOZP=11
inZWN=13
in15=15
in19=19
in21=21

#temperature sensor pin setup
cs=22
sck=18
so=16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inPM, GPIO.OUT)
GPIO.setup(inPD, GPIO.OUT)
GPIO.setup(inPWC, GPIO.OUT)
GPIO.setup(inOZP, GPIO.OUT)
GPIO.setup(inZWN, GPIO.OUT)
GPIO.setup(in15, GPIO.OUT)
GPIO.setup(in19, GPIO.OUT)
GPIO.setup(in21, GPIO.OUT)

GPIO.output(inPM, True)
GPIO.output(inPD, True)
GPIO.output(inPWC, True)
GPIO.output(inOZP, True)
GPIO.output(inZWN, True)
GPIO.output(in15, True)
GPIO.output(in19, True)
GPIO.output(in21, True)

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, height=600, width=1050)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        frame1 = tk.LabelFrame(self, text="Parametry Pracy")
        frame1.place(rely=0.05, relx=0.02, height=400, width=400)
        #frame1.grid_columnconfigure(2,1)
        #frame1.grid_rowconfigure(4,1)

        pp=tk.Frame(frame1)
        pp.pack(pady=2)

        def zegar():
            string = strftime('%H:%M:%S')
            lbl.config(text=string)
            lbl.after(1000, zegar)

        # Styling the label widget so that clock
        # will look more attractive
        lbl = Label(pp, font=('arial', 40, 'bold'), width=8)
        lbl.grid(row=0, column=0, columnspan=2, sticky="W", padx=5)
        
        zegar()
        
        def tempc():
            # max6675.set_pin(CS, SCK, SO, unit)   [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
            max6675.set_pin(cs, sck, so, 1)                          
            tstring = round(max6675.read_temp(cs),1)
            tpp.config(text=tstring)
            tpp.after(1000, tempc)
         
        #Thermomether label
        ltpp = Label(pp, text="Temperatura pompy dyfuzyjnej")
        ltpp.grid(row=1, column=0, sticky="W", padx=10)
        
        #grid pos. for temperature indicator
        tpp = Label(pp, font=('arial', 40, 'bold'), width=4)
        tpp.grid(row=2, column=0, sticky="W", padx=10)
        tempc()
        
        #add C after temperature value
        
        ltppc = Label(pp, font=('arial', 40, 'bold'), width=2, text='\u00b0'"C")
        ltppc.grid(row=2, column=1, sticky="W", padx=10)        
        pg=BGP400_RS232("/dev/serial0")
        #Vacuum indicator
        def Inficon(pg):
            #try:
                with BGP400_RS232("/dev/serial0") as pg:
                    #while True:
                        pressure = pg.get_pressure(PressureGaugeUnit.MBAR)
                        print(pressure)
                        if pressure is not None:
                            #print(round(pressure))
                            vpp.config(text=round(pressure))
                            vpp.after(1000,Inficon)
                            vpp=Label(pp, font=('arial', 40, 'bold'), width=6)
                            vpp.grid(row=4, column=0, sticky="W", padx=10)
                                                           
                            #ltpv = Label(pp, font=('arial', 40, 'bold'), width=6, text="mBAR")
                            #ltpv.grid(row=4, column=1, sticky="W", padx=10)
                                                    
                        else:
                            #print(pressure)
                            ltpb=Label(pp, text = str(pressure), font=('arial', 40, 'bold'), width=6)
                            ltpb.grid(row=4, column=0, sticky="W", padx=10)
                            ltpb.after(1000, Inficon)
            #except KeyboardInterrupt:
                #print ("measurement stopped by user")
                           
        #Vacuum pressure label
        lpv = Label(pp, text="Próżnia")
        lpv.grid(row=3, column=0, sticky="W", padx=10)
        Inficon()
               

        frame2 = tk.LabelFrame(self, text="Właczanie modułów")
        frame2.place(rely=0.05, relx=0.42, height=400, width=550)
           

        blf = tk.Frame(frame2)
        blf.pack(pady=2)

        #def led (self):
            #ledon = Image.open('Led Ziel.png')
            #ledon = ImageTk.PhotoImage(ledon)
            #logo_label = tk.Label(image=ledon)
            #logo_label.image = ledon
            #logo_label.grid(column=1, row=0)

        l1 = tk.Label(blf, text="Pompa Mechaniczna")
        l1.grid(row=0, column=1, sticky="W", padx=20)

        l2 = tk.Label(blf, text="Pompa Dyfuzyjna")
        l2.grid(row=1, column=1, sticky="W", padx=20)

        l3 = tk.Label(blf, text="Pompa Wody Chłodzącej")
        l3.grid(row=2, column=1, sticky="W", padx=20)

        l4 = tk.Label(blf, text="Zasilanie Sondy Próżniowej")
        l4.grid(row=3, column=1, sticky="W", padx=20)

        l5 = tk.Label(blf, text="Zasilanie Wysokiego Napięcia")
        l5.grid(row=4, column=1, sticky="W", padx=20)

        button1 = tk.Button(blf, text="START", command=lambda:GPIO.output(inPM, False))
        button1.grid(row=0, column=2, padx=20, pady=20)

        button2 = tk.Button(blf, text="STOP", command=lambda:GPIO.output(inPM, True))
        button2.grid(row=0, column=3, padx=20, pady=20)

        button3 = tk.Button(blf, text="START", command=lambda:GPIO.output(inPD, False))
        button3.grid(row=1, column=2, padx=20, pady=20)

        button4 = tk.Button(blf, text="STOP", command=lambda:GPIO.output(inPD, True))
        button4.grid(row=1, column=3, padx=20, pady=20)

        button5 = tk.Button(blf, text="START", command=lambda:GPIO.output(inPWC, False))
        button5.grid(row=2, column=2, padx=20, pady=20)

        button6 = tk.Button(blf, text="STOP", command=lambda:GPIO.output(inPWC, True))
        button6.grid(row=2, column=3, padx=20, pady=20)

        button7 = tk.Button(blf, text="START", command=lambda:GPIO.output(inOZP, False))
        button7.grid(row=3, column=2, padx=20, pady=20)

        button8 = tk.Button(blf, text="STOP", command=lambda:GPIO.output(inOZP, True))
        button8.grid(row=3, column=3, padx=20, pady=20)

        button9 = tk.Button(blf, text="START", command=lambda:GPIO.output(inZWN, False))
        button9.grid(row=4, column=2, padx=20, pady=20)

        button10 = tk.Button(blf, text="STOP", command=lambda:GPIO.output(inZWN, True))
        button10.grid(row=4, column=3, padx=20, pady=20)
        
        def check_mechanical_pump():
            state_mechanical_pump=GPIO.input(inPM)
            #print(state_mechanical_pump)
            if state_mechanical_pump == 0:
                on = Image.open("Ikony/LedG.png")
                on = on.resize((70,70))
                on_img = ImageTk.PhotoImage(on)
                label_mechanical_pump=Label(blf, image=on_img)
                label_mechanical_pump.image=on_img
                label_mechanical_pump.grid(row=0, column=4, sticky="W", padx=10)
                label_mechanical_pump.after(1000,check_mechanical_pump)
            else:
                off = Image.open("Ikony/LedR.png")
                off = off.resize((70,70))
                off_img = ImageTk.PhotoImage(off)
                label_mechanical_pump=Label(blf, image=off_img)
                label_mechanical_pump.image=off_img
                label_mechanical_pump.grid(row=0, column=4, sticky="W", padx=10)
                label_mechanical_pump.after(1000,check_mechanical_pump)
        check_mechanical_pump()
        
        def check_diffusion_pump():
            state_diffusion_pump=GPIO.input(inPD)
            #print(state_diffusion_pump)
            if state_diffusion_pump == 0:
                on = Image.open("Ikony/LedG.png")
                on = on.resize((70,70))
                on_img = ImageTk.PhotoImage(on)
                label_diffusion_pump=Label(blf, image=on_img)
                label_diffusion_pump.image=on_img
                label_diffusion_pump.grid(row=1, column=4, sticky="W", padx=10)
                label_diffusion_pump.after(1000,check_diffusion_pump)
            else:
                off = Image.open("Ikony/LedR.png")
                off = off.resize((70,70))
                off_img = ImageTk.PhotoImage(off)
                label_diffusion_pump=Label(blf, image=off_img)
                label_diffusion_pump.image=off_img
                label_diffusion_pump.grid(row=1, column=4, sticky="W", padx=10)
                label_diffusion_pump.after(1000,check_diffusion_pump)
        check_diffusion_pump()    
        
        def check_cooling_water_pump():
            state_cooling_water_pump=GPIO.input(inPWC)
            #print(state_cooling_water_pump)
            if state_cooling_water_pump == 0:
                on = Image.open("Ikony/LedG.png")
                on = on.resize((70,70))
                on_img = ImageTk.PhotoImage(on)
                label_cooling_water_pump=Label(blf, image=on_img)
                label_cooling_water_pump.image=on_img
                label_cooling_water_pump.grid(row=2, column=4, sticky="W", padx=10)
                label_cooling_water_pump.after(1000,check_cooling_water_pump)
            else:
                off = Image.open("Ikony/LedR.png")
                off = off.resize((70,70))
                off_img = ImageTk.PhotoImage(off)
                label_cooling_water_pump=Label(blf, image=off_img)
                label_cooling_water_pump.image=off_img
                label_cooling_water_pump.grid(row=2, column=4, sticky="W", padx=10)
                label_cooling_water_pump.after(1000,check_cooling_water_pump)
        check_cooling_water_pump()
        
        def check_power_vacuum_gauge():
            state_power_vacuum_gauge=GPIO.input(inOZP)
            #print(state_power_vacuum_gauge)
            if state_power_vacuum_gauge == 0:
                on = Image.open("Ikony/LedG.png")
                on = on.resize((70,70))
                on_img = ImageTk.PhotoImage(on)
                label_power_vacuum_gauge=Label(blf, image=on_img)
                label_power_vacuum_gauge.image=on_img
                label_power_vacuum_gauge.grid(row=3, column=4, sticky="W", padx=10)
                label_power_vacuum_gauge.after(1000,check_power_vacuum_gauge)
            else:
                off = Image.open("Ikony/LedR.png")
                off = off.resize((70,70))
                off_img = ImageTk.PhotoImage(off)
                label_power_vacuum_gauge=Label(blf, image=off_img)
                label_power_vacuum_gauge.image=off_img
                label_power_vacuum_gauge.grid(row=3, column=4, sticky="W", padx=10)
                label_power_vacuum_gauge.after(1000,check_power_vacuum_gauge)
        check_power_vacuum_gauge() 
        
        def check_state_high_voltage():
            state_high_voltage=GPIO.input(inZWN)
            #print(state_high_voltage)
            if state_high_voltage == 0:
                on = Image.open("Ikony/LedG.png")
                on = on.resize((70,70))
                on_img = ImageTk.PhotoImage(on)
                label_state_high_voltage=Label(blf, image=on_img)
                label_state_high_voltage.image=on_img
                label_state_high_voltage.grid(row=4, column=4, sticky="W", padx=10)
                label_state_high_voltage.after(1000,check_state_high_voltage)
            else:
                off = Image.open("Ikony/LedR.png")
                off = off.resize((70,70))
                off_img = ImageTk.PhotoImage(off)
                label_state_high_voltage=Label(blf, image=off_img)
                label_state_high_voltage.image=off_img
                label_state_high_voltage.grid(row=4, column=4, columnspan=3, rowspan=3, sticky="W", padx=10)
                label_state_high_voltage.after(1000,check_state_high_voltage)
        check_state_high_voltage()


        #frame3 = tk.LabelFrame(self, text="Parametry Przełączania")
        #frame3.place(rely=5, relx=0.42, height=100, width=550)
        #ppr = tk.Frame(frame3)
        #ppr.pack(pady=2)


root = MainWindow()
root.title("Syndam")
#pressureString = StringVar()
#pressureString.set("---mbar")
#pressureLabel = Label(root, textvariable = pressureString)
#root.after(1000, Vacuum, root, pressureString)
root.mainloop()

