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

    #in1 = "/home/jaroslav/sim/lmon/data/luminosity/lm1a/hits.root"
    in1 = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax1/hits.root"
    in2 = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax2/hits.root"
    #in2 = "/home/jaroslav/sim/lmon/data/luminosity/lm1b/hits.root"
    in3 = "/home/jaroslav/sim/lmon/data/luminosity/lm1c/hits.root"

    en1 = get_en(in1)
    en2 = get_en(in2)
    #en3 = get_en(in3, 0.6)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    #fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(en1[0], en1[1], "-", color="red", lw=1)
    plt.plot(en2[0], en2[1], "-", color="gold", lw=1)
    #plt.plot(en3[0], en3[1], "-", color="blue", lw=1)

    ax.set_xlabel("Incident energy in bunch crossing (GeV)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    leg = legend()
    leg.add_entry(leg_txt(), "CAL$_\mathrm{up}$ + CAL$_\mathrm{down}$")
    leg.add_entry(leg_txt(), "CAL$_\mathrm{up}$ > 1 && CAL$_\mathrm{down}$ > 1 GeV")
    leg.add_entry(leg_lin("red"), "18x275 GeV")
    leg.add_entry(leg_lin("gold"), "10x100 GeV")
    leg.add_entry(leg_lin("blue"), "5x41 GeV")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#main

#_____________________________________________________________________________
def get_en(infile, ebin=0.5):

    emax = 100.

    inp_lmon = TFile.Open(infile)
    tree = inp_lmon.Get("bunch")

    hE = ut.prepare_TH1D("hE", ebin, 0, emax)
    #tree.Draw("bun_up_en+bun_down_en >> hE", "(bun_up_en>1)&&(bun_down_en>1)", "", 1000)
    tree.Draw("bun_up_en+bun_down_en >> hE", "(bun_up_en>1)&&(bun_down_en>1)")
    ut.norm_to_integral(hE, 1.)

    return ut.h1_to_arrays(hE)

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


