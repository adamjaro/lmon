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

    iplot = 0

    func = {}
    func[0] = xres

    func[iplot]()

#main

#_____________________________________________________________________________
def xres():

    #position resolution

    #mm
    xmin = -20
    xmax = 20
    xbin = 2

    infile = "bpc.root"
    inp = TFile.Open(infile)
    tree = inp.Get("bpc")

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)
    tree.Draw("xrec >> hx")
    ut.norm_to_integral(hx, 1)

    xp, yp = ut.h1_to_arrays(hx)

    #Gaussian fit
    cen = []
    val = []
    for i in range(1, hx.GetNbinsX()+1):
        cen.append( hx.GetBinCenter(i) )
        val.append( hx.GetBinContent(i) )

    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), cen, val)

    #print(cen, val)

    #fit function
    x = np.linspace(cen[0], cen[-1], 300)
    y = norm.pdf(x, pars[0], pars[1])

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
    plt.plot(x, y, "-", color="red", lw=1)

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("counts")

    #ax.set_yscale("log")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "mean: {0:.3f}".format(pars[0]))
    leg.add_entry(leg_txt(), "sigma: {0:.3f}".format(pars[1]))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#xres

#_____________________________________________________________________________
def set_axes_color(ax, col):

    #[t.set_color('red') for t in ax.xaxis.get_ticklines()]
    #[t.set_color('red') for t in ax.xaxis.get_ticklabels()]

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

    main()




























