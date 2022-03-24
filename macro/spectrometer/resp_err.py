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

    iplot = 2

    func = {}
    func[0] = en_err
    func[1] = theta_err
    func[2] = phi_err

    func[iplot]()

#_____________________________________________________________________________
def en_err():

    #relative error in energy

    xbin = 0.01
    xmin = 0
    xmax = 1

    inp = "~/sim/lmon/analysis/ini/spect_resp.root"
    #inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = make_h1(inp, "spec_links", "en_err/en", xbin, xmin, xmax, "ninp>1")
    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel("$sE/E$")
    ax.set_ylabel("Normalized counts")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#en_err

#_____________________________________________________________________________
def theta_err():

    #relative error in theta

    xbin = 0.001
    xmin = 0
    xmax = 1

    inp = "~/sim/lmon/analysis/ini/spect_resp.root"
    #inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = make_h1(inp, "spec_links", "theta_err/theta", xbin, xmin, xmax, "ninp>1")
    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel("$sT/T$")
    ax.set_ylabel("Normalized counts")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#theta_err

#_____________________________________________________________________________
def phi_err():

    #relative error in energy

    xbin = 0.01
    xmin = 0
    xmax = 1

    inp = "~/sim/lmon/analysis/ini/spect_resp.root"
    #inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = make_h1(inp, "spec_links", "phi_err/phi", xbin, xmin, xmax, "ninp>1")
    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel("$sE/E$")
    ax.set_ylabel("Normalized counts")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#phi_err

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax, sel=""):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    #hx = ut.prepare_TH1D(tnam+"_"+val+"_hx", xbin, xmin, xmax)
    #tree.Draw(val+" >> "+tnam+"_"+val+"_hx", sel)
    hx = ut.prepare_TH1D(tnam+"_hx", xbin, xmin, xmax)
    tree.Draw(val+" >> "+tnam+"_hx", sel)

    print(val, "entries:", hx.GetEntries())

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




