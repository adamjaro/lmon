#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = radial

    func[iplot]()

#main

#_____________________________________________________________________________
def radial():

    #Hz
    #total_rate = 685833. # full range
    #total_rate = 594328. # z > 0
    #total_rate = 463719. # z > 3600 mm
    total_rate = 388011. # z > 5000 mm

    #all simulated events
    #nall = 10e6 # full range
    #nall = 8671142 # z > 0
    #nall = 6779283 # z > 3600 mm
    nall = 5679573 # z > 5000 mm

    #photon and electron rate
    #xp, yp = get_rate("rc_z0_zcut.root", total_rate, nall)
    #exp, eyp = get_rate("rc_el_z0_zcut.root", total_rate, nall)
    #xp, yp = get_rate("rc_ecal_zcut.root", total_rate, nall)
    #exp, eyp = get_rate("rc_el_ecal_zcut.root", total_rate, nall)
    xp, yp = get_rate("rc_hcal_zcut.root", total_rate, nall)
    exp, eyp = get_rate("rc_el_hcal_zcut.root", total_rate, nall)
    #xp, yp = get_rate("rc_hcal.root", total_rate, nall)
    #exp, eyp = get_rate("rc_el_hcal.root", total_rate, nall)

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xp, yp, "-", color="blue", lw=1)
    plt.plot(exp, eyp, "-", color="red", lw=1)

    ax.set_xlabel("$r_{xy}$ (cm) at $z$ = 0")
    ax.set_ylabel("Event rate (Hz) in $\delta r$ = 1 cm")

    leg = legend()
    #leg.add_entry(leg_txt(), "Plane at $z$ = 0, radial intervals $\delta r$ = 1 cm")
    #leg.add_entry(leg_txt(), "Plane at $z$ = 3.6 m, radial intervals $\delta r$ = 1 cm")
    leg.add_entry(leg_txt(), "Plane at $z$ = 5 m, radial intervals $\delta r$ = 1 cm")
    leg.add_entry(leg_lin("red"), "Electron rate")
    leg.add_entry(leg_lin("blue"), "Photon rate")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#radial

#_____________________________________________________________________________
def get_rate(infile, total_rate, nall):

    #cm
    rmin = 3.2
    rmax = 70
    rbin = 1

    infile = TFile.Open(infile)
    tree = infile.Get("rtree")

    print("Tree entries:", tree.GetEntries())

    hr = ut.prepare_TH1D("hr", rbin, rmin, rmax)

    tree.Draw("rpos/1e1 >> hr", "rpos>"+str(rmin*10))

    print("Plot entries:", hr.GetEntries())

    #rate per simulated event
    rsim = total_rate/nall
    print("rsim:", rsim)

    xp = []
    yp = []
    all_rate = 0.
    for ibin in range(1,hr.GetNbinsX()+1):
        xp.append( hr.GetBinLowEdge(ibin) )
        xp.append( hr.GetBinLowEdge(ibin) + hr.GetBinWidth(ibin) )

        #rate in a given bin
        rate = rsim*hr.GetBinContent(ibin)
        #print(rate)

        yp.append( rate )
        yp.append( rate )

        all_rate += rate

    print("Integrated rate:", all_rate)

    return xp, yp

#get_rate

#_____________________________________________________________________________
def set_axes_color(ax, col):

    ax.xaxis.label.set_color(col)
    ax.yaxis.label.set_color(col)
    ax.tick_params(which = "both", colors = col)
    ax.spines["bottom"].set_color(col)
    ax.spines["left"].set_color(col)
    ax.spines["top"].set_color(col)
    ax.spines["right"].set_color(col)

#set_axes_color

#_____________________________________________________________________________
def set_grid(px, col="lime"):

    px.grid(True, color = col, linewidth = 0.5, linestyle = "--")

#set_grid

#_____________________________________________________________________________
class legend:
    def __init__(self):
        self.items = []
        self.data = []
    def add_entry(self, i, d):
        self.items.append(i)
        self.data.append(d)
    def draw(self, px, col=None, **kw):
        leg = px.legend(self.items, self.data, **kw)
        if col != None:
            px.setp(leg.get_texts(), color=col)
            if col != "black":
                leg.get_frame().set_edgecolor("orange")
        return leg

#_____________________________________________________________________________
def leg_lin(col, sty="-"):
    return Line2D([0], [0], lw=2, ls=sty, color=col)

#_____________________________________________________________________________
def leg_txt():
    return Line2D([0], [0], lw=0)

#_____________________________________________________________________________
def leg_dot(fig, col, siz=8):
    return Line2D([0], [0], marker="o", color=fig.get_facecolor(), markerfacecolor=col, markersize=siz)

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()




















