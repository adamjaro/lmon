
from telnetlib import Telnet
from time import sleep
from pandas import DataFrame
from math import sqrt

#_____________________________________________________________________________
class E4980A:
    #_____________________________________________________________________________
    def __init__(self, ip, port):

        #range and steps in bias voltage, V
        self.vmin = 1
        self.vmax = 28
        self.npoints = 120

        #output name
        self.out_nam = "out.csv"

        #number of measurements for average
        self.navg = 12

        #data for output DataFrame
        self.out = {"Vb_V":[], "Cp_F":[], "Rp_Ohm":[], "Vdc_V":[], "Idc_A":[],\
                    "Cp_err":[], "Rp_err":[], "Vdc_err":[], "Idc_err":[]}

        #telnet session for the meter
        self.telnet = Telnet()
        self.telnet.open(ip, port)

        #clean the welcome message
        self.telnet.read_until(b">")

    #__init__

    #_____________________________________________________________________________
    def run(self):

        #turn bias on
        self.put(":BIAS:STAT ON")

        #run the measurement procedure
        for vb in [self.vmin+i*(self.vmax-self.vmin)/(self.npoints-1) for i in range(self.npoints)]:
            print("Vbias (V):", vb)

            #apply the bias
            self.put(":BIAS:VOLT "+str(vb))
            self.out["Vb_V"].append(vb)
            sleep(0.3)

            #read the data
            dat = {"cp":[], "rp":[], "vdc":[], "idc":[]}

            #average loop
            for iavg in range(self.navg):
                #trigger the meter
                self.put(":TRIG")

                #load the results
                cprp = self.put(":FETC?").split(",")
                dat["cp"].append( float(cprp[0]) )
                dat["rp"].append( float(cprp[1]) )
                dat["vdc"].append( float(self.put(":FETC:SMON:VDC?")) )
                dat["idc"].append( float(self.put(":FETC:SMON:IDC?")) )

            #calculate the averages
            df = DataFrame(dat)

            #set the output, mean values
            self.out["Cp_F"].append( df["cp"].mean() )
            self.out["Rp_Ohm"].append( df["rp"].mean() )
            self.out["Vdc_V"].append( df["vdc"].mean() )
            self.out["Idc_A"].append( df["idc"].mean() )

            #standard deviation of the mean
            self.out["Cp_err"].append( df["cp"].std()/sqrt(self.navg) )
            self.out["Rp_err"].append( df["rp"].std()/sqrt(self.navg) )
            self.out["Vdc_err"].append( df["vdc"].std()/sqrt(self.navg) )
            self.out["Idc_err"].append( df["idc"].std()/sqrt(self.navg) )

        #ramp down and turn bias off
        self.ramp_down()

        #write the output
        out_df = DataFrame(self.out)
        print(out_df)
        out_df.to_csv(self.out_nam)

        #close the telnet session
        self.telnet.close()

    #_____________________________________________________________________________
    def configure(self):

        #configure for CpRp measurement
        self.put(":FUNC:IMP CPRP")
        self.put(":FREQ 10KHZ")
        self.put(":VOLT 0.05")
        self.put(":APER LONG,1")
        self.put(":TRIG:SOUR HOLD")
        self.put(":BIAS:VOLT 0")
        self.put(":FUNC:SMON:VDC ON")
        self.put(":FUNC:SMON:IDC ON")
        self.put(":FORM:ASC:LONG ON")

    #_____________________________________________________________________________
    def ramp_down(self):

        #ramp down the bias voltage to zero and turn the bias off

        print("Ramp down")

        # 1 V/sec
        while True:

            vb = float(self.put(":BIAS:VOLT?"))
            vb -= 1
            if vb <= 0: break

            print("Rdown, Vb (V):", vb)
            self.put(":BIAS:VOLT "+str(vb))
            sleep(1)

        #adjust to zero and turn off
        self.put(":BIAS:VOLT 0")
        self.put(":BIAS:STAT OFF")

    #_____________________________________________________________________________
    def put(self, cmd):

        #put a command to the meter and get the response

        cmd += "\n"
        for i in cmd:
            self.telnet.write( bytes(i, "utf-8") )

        #take the response and remove formatting characters
        resp = self.telnet.read_until(b">").decode("utf-8")
        resp = resp.replace(" :", "")
        resp = resp.replace("\r\nSCPI>", "")

        return resp


