#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile

import sys
sys.path.append('../')

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np

import plot_utils as ut
from BoxCalV2Hits import BoxCalV2Hits

#_____________________________________________________________________________
def main():

    iplot = 0
    funclist = []
    funclist.append( hits_xy ) # 0
    funclist.append( hits_z ) # 1
    funclist.append( fit_x ) # 2
    funclist.append( fit_y ) # 3

    funclist[iplot]()

#main

#_____________________________________________________________________________
def hits_xy():

    #input
    infile = "../../lmon.root"

    #Q3eR location
    xpos = -460.03 # mm
    #xpos = -(470.87+460.03)/2 # mm
    #xpos = -460.03 # mm
    zpos = -37700 # mm
    #zpos = -38300 # mm
    rot_y = 0.01808 # rad

    #plot range
    #xybin = 0.3
    xybin = 0.1
    xylen = 20

    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    hits = BoxCalV2Hits("Q3eR", tree)

    nevt = -300000

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xylen, xylen, xybin, -xylen, xylen)

    if nevt < 0:
        nevt = tree.GetEntries()
    for ievt in range(nevt):
        tree.GetEntry(ievt)

        for ihit in range(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)
            #hit.GlobalToLocal(xpos, 0, zpos)

            #print(hit.x, hit.y)
            hXY.Fill(hit.x, hit.y)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    ytit = "#it{y} (mm)"
    xtit = "#it{x} (mm)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_xy

#_____________________________________________________________________________
def hits_z():

    #input
    infile = "../../lmon.root"

    #Q3eR location
    xpos = -460.03 # mm
    zpos = -37700 # mm
    rot_y = 0.01808 # rad
    #rot_y = 0.11

    #plot range
    zbin = 0.1
    zmax = 3

    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    hits = BoxCalV2Hits("Q3eR", tree)

    nevt = 120

    can = ut.box_canvas()
    hZ = ut.prepare_TH1D("hz", zbin, -zmax, zmax)

    if nevt < 0:
        nevt = tree.GetEntries()

    for ievt in range(nevt):
        tree.GetEntry(ievt)

        print(hits.GetN())

        for ihit in range(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)
            #hit.GlobalToLocal(xpos, 0, zpos)

            hZ.Fill(hit.z)

    hZ.Draw()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_z

#_____________________________________________________________________________
def fit_x():

    #input
    infile = "../../lmon.root"

    #Q3eR location
    xpos = -460.03 # mm
    #xpos = 0 # mm
    zpos = -37700 # mm
    #xpos = -465.450 # mm
    #zpos = -38000 # mm
    #xpos = -470.87 # mm
    #zpos = -38300 # mm
    rot_y = 0.01808 # rad

    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    hits = BoxCalV2Hits("Q3eR", tree)

    nevt = -12

    xval = []
    if nevt < 0:
        nevt = tree.GetEntries()
    for ievt in range(nevt):
        tree.GetEntry(ievt)

        for ihit in range(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)

            xval.append(hit.x)

    nbins = 60

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = plt.hist(xval, bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, hx[0])

    #print(pars[0], 3*pars[1])

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    plt.plot(x, y, "-", label="norm", color="red")

    ax.set_xlabel("$x$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "$\mu_x$ (mm): {0:.3f} $\pm$ {1:.3f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "3$\sigma_x$ (mm): {0:.3f} $\pm$ {1:.3f}".format( 3.*pars[1], 3.*np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#fit_x

#_____________________________________________________________________________
def fit_y():

    #input
    infile = "../../lmon.root"

    #Q3eR location
    xpos = -460.03 # mm
    #xpos = 0 # mm
    zpos = -37700 # mm
    rot_y = 0.01808 # rad

    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    hits = BoxCalV2Hits("Q3eR", tree)

    nevt = -12

    yval = []
    if nevt < 0:
        nevt = tree.GetEntries()
    for ievt in range(nevt):
        tree.GetEntry(ievt)

        for ihit in range(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)

            yval.append(hit.y)

    nbins = 60

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hy = plt.hist(yval, bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hy[1][1:]+hy[1][:-1]))
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, hy[0])

    #print(pars[0], 3*pars[1])

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    plt.plot(x, y, "-", label="norm", color="red")

    ax.set_xlabel("$y$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "$\mu_y$ (mm): {0:.3f} $\pm$ {1:.3f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "3$\sigma_y$ (mm): {0:.3f} $\pm$ {1:.3f}".format( 3.*pars[1], 3.*np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#fit_y

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

















