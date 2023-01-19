
from telnetlib import Telnet
from time import sleep
from pandas import DataFrame
from math import sqrt

from ctypes import c_double
from ROOT import TFile, TTree

#_____________________________________________________________________________
class E4980A:
    #_____________________________________________________________________________
    def __init__(self, ip, port):

        #range and steps in bias voltage, V
        self.vmin = 1
        self.vmax = 11
        self.npoints = 4

        #output name
        out = "out.root"

        #number of measurements for average
        self.navg = 3

        #create the output
        self.outfile = TFile(out, "recreate")
        self.tree = TTree("CpRp", "CpRp")
        self.vbias = c_double()
        self.cp = c_double()
        self.rp = c_double()
        self.vdc = c_double()
        self.idc = c_double()
        self.cp_err = c_double()
        self.rp_err = c_double()
        self.vdc_err = c_double()
        self.idc_err = c_double()
        self.tree.Branch("bias", self.vbias, "bias/D")
        self.tree.Branch("cp", self.cp, "cp/D")
        self.tree.Branch("rp", self.rp, "rp/D")
        self.tree.Branch("vdc", self.vdc, "vdc/D")
        self.tree.Branch("idc", self.idc, "idc/D")
        self.tree.Branch("cp_err", self.cp_err, "cp_err/D")
        self.tree.Branch("rp_err", self.rp_err, "rp_err/D")
        self.tree.Branch("vdc_err", self.vdc_err, "vdc_err/D")
        self.tree.Branch("idc_err", self.idc_err, "idc_err/D")

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
            self.vbias.value = vb
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
            self.cp.value = df["cp"].mean()
            self.rp.value = df["rp"].mean()
            self.vdc.value = df["vdc"].mean()
            self.idc.value = df["idc"].mean()

            #standard deviation of the mean
            self.cp_err.value = df["cp"].std()/sqrt(self.navg)
            self.rp_err.value = df["rp"].std()/sqrt(self.navg)
            self.vdc_err.value = df["vdc"].std()/sqrt(self.navg)
            self.idc_err.value = df["idc"].std()/sqrt(self.navg)

            #fill the output
            self.tree.Fill()

        #ramp down and turn bias off
        self.ramp_down()

        #write the output
        self.tree.Write()
        self.outfile.Close()

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


