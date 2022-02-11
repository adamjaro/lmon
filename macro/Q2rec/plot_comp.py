#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = lq_rec
    func[1] = lq_compare

    func[iplot]()

#main

#_____________________________________________________________________________
def lq_rec():

    #spectrum of reconstructed log_10(Q^2)

    #infile = "/home/jaroslav/sim/lmon/data/taggers/tag1a/Q2rec_s1.root"
    #infile = "/home/jaroslav/sim/lmon/data/taggers/tag1a/Q2rec_s2.root"
    #infile = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/Q2rec_s1.root"
    #infile = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/Q2rec_s2.root"
    #infile = "/home/jaroslav/sim/lmon/data/luminosity/lm2ax2/Q2rec_s1.root"
    infile = "/home/jaroslav/sim/lmon/data/luminosity/lm2ax2/Q2rec_s2.root"

    #range along x in log_10(Q^2) (GeV^2)
    xmin = -10
    xmax = -1
    xbin = 0.1

    inp = TFile.Open(infile)
    tree = inp.Get("Q2rec")

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)
    tree.Draw("rec_lq >> hx")
    ut.norm_to_integral(hx, 1)

    xp, yp = ut.h1_to_arrays(hx)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xp, yp, "-", color="blue", lw=1)

    ax.set_xlabel("lQ2 (GeV2)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    #plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.0f}".format(i+6)+"}$" for i in ax.get_xticks()[1:-1]])

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#_____________________________________________________________________________
def lq_compare():

    #input, color, rate in MHz by taggers/hit_rate.py
    #Tagger 1
    inp_s1 = [\
        {"in": "/home/jaroslav/sim/lmon/data/luminosity/lm2ax2/Q2rec_s1.root", "col": "red", "rate": 19.1405, "lab": "Bremsstrahlung"}, \
        {"in": "/home/jaroslav/sim/lmon/data/taggers/tag1a/Q2rec_s1.root", "col": "blue", "rate": 0.002905, "lab": "Quasi-real"}, \
        {"in": "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/Q2rec_s1.root", "col": "orange", "rate": 0.004053, "lab": "Pythia6"} \
    ]
    #Tagger 2
    inp_s2 = [\
        {"in": "/home/jaroslav/sim/lmon/data/luminosity/lm2ax2/Q2rec_s2.root", "col": "red", "rate": 22.0011, "lab": "Bremsstrahlung"}, \
        {"in": "/home/jaroslav/sim/lmon/data/taggers/tag1a/Q2rec_s2.root", "col": "blue", "rate": 0.005642, "lab": "Quasi-real"}, \
        {"in": "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/Q2rec_s2.root", "col": "orange", "rate": 0.008656, "lab": "Pythia6"} \
    ]

    #tnam = "Tagger 1"
    #inp = inp_s1

    tnam = "Tagger 2"
    inp = inp_s2

    #range along x in log_10(Q^2) (GeV^2)
    xmin = -10
    xmax = -1
    xbin = 0.1

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
    leg.add_entry(leg_txt(), tnam)

    #inputs loop
    for i in inp:

        infile = TFile.Open(i["in"])
        tree = infile.Get("Q2rec")

        hx = ut.prepare_TH1D("hx_"+i["col"], xbin, xmin, xmax)
        tree.Draw("rec_lq >> hx_"+i["col"])
        ut.norm_to_integral(hx, i["rate"])

        xp, yp = ut.h1_to_arrays(hx)
        leg.add_entry(leg_lin(i["col"]), i["lab"])

        plt.plot(xp, yp, "-", color=i["col"], lw=1)

    ax.set_xlabel("Reconstructed log$_{10}(Q^2)$ (GeV$^2$)")
    ax.set_ylabel("Counts normalized to event rate in MHz")

    ax.set_yscale("log")

    #plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.0f}".format(i+6)+"}$" for i in ax.get_xticks()[1:-1]])

    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#lq_compare

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
        if col is not None:
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

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()



























