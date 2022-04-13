#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = dxy

    func[iplot]()

#_____________________________________________________________________________
def dxy():

    #distribution in Delta_xy for hit pairs

    #mm
    #xbin = 1
    #xmax = 180
    xbin = 0.1
    xmax = 10

    #det = "s1"
    det = "s2"

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5ax1/hits_tag.root"

    planes = [{"in": det+"A_pairs", "col": "red", "lab": "Plane A"},\
        {"in": det+"B_pairs", "col": "blue", "lab": "Plane B"},\
        {"in": det+"C_pairs", "col": "orange", "lab": "Plane C"}\
    ]

    ltit = {"s1": "Tagger 1", "s2": "Tagger 2"}

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    leg.add_entry(leg_txt(), ltit[det])

    infile = TFile.Open(inp)

    for i in planes:

        hx = make_h1(inp, i["in"], "dxy", xbin, 0, xmax)

        plt.plot(hx[0], hx[1], "-", color=i["col"], lw=1)

        leg.add_entry(leg_lin(i["col"]), i["lab"])

        #fraction of distances below a selection
        tx = infile.Get(i["in"])
        xall = float(tx.GetEntries())
        xsel = float( tx.Draw("", "dxy<0.5") )
        xsel2 = float( tx.Draw("", "dxy<0.3") )
        print(i["in"], xsel/xall, xsel2/xall)

    ax.set_xlabel("$\Delta_{xy}$ (mm)")
    ax.set_ylabel("Normalized counts")

    #ax.set_yscale("log")

    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#dxy

#_____________________________________________________________________________
def hit_rate():

    #hit rate in simulated bunch crossings
    pass

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax, sel=""):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    hx = ut.prepare_TH1D(tnam+"_hx", xbin, xmin, xmax)
    tree.Draw(val+" >> "+tnam+"_hx", sel)
    ut.norm_to_integral(hx, 1.)

    return ut.h1_to_arrays(hx)

#make_h1

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


