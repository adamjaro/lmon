#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = zpos
    func[1] = radial

    func[iplot]()

#main

#_____________________________________________________________________________
def zpos():

    in1 = "/home/jaroslav/sim/lmon/data/luminosity/lm1a/hits.root"
    in2 = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax1/hits.root"

    zbin = 0.1
    zmin = -2000
    zmax = 2000

    #det = "phot"
    #det = "up"
    det = "down"

    #val = "z"
    val = "z+37175"

    z1 = make_h1(in1, det, val, zbin, zmin, zmax)
    z2 = make_h1(in2, det, val, zbin, zmin, zmax)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(z1[0], z1[1], "-", color="red", lw=1)
    plt.plot(z2[0], z2[1], "-", color="gold", lw=1)

    ax.set_xlabel("$z$ (mm)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#zpos

#_____________________________________________________________________________
def radial():

    in1 = "/home/jaroslav/sim/lmon/data/luminosity/lm1a/hits.root"
    in2 = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax1/hits.root"

    rbin = 1
    rmin = 0
    rmax = 200

    det = "phot"
    #det = "up"
    #det = "down"

    val = "TMath::Sqrt(x*x+y*y)"

    r1 = make_h1(in1, det, val, rbin, rmin, rmax)
    r2 = make_h1(in2, det, val, rbin, rmin, rmax)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(r1[0], r1[1], "-", color="red", lw=1)
    plt.plot(r2[0], r2[1], "-", color="gold", lw=1)

    ax.set_xlabel("$z$ (mm)")
    ax.set_ylabel("Normalized counts")

    #ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#radial

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)
    tree.Draw(val+" >> hx")
    #ut.norm_to_integral(hx, 1.)

    return ut.h1_to_arrays(hx)

#get_en

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

