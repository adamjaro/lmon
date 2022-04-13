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

    iplot = 3

    func = {}
    func[0] = x
    func[1] = y
    func[2] = theta_x
    func[3] = theta_y
    func[4] = calE
    func[5] = true_E
    func[6] = true_pitheta
    func[7] = true_phi

    func[iplot]()

#_____________________________________________________________________________
def x():

    #x position on spectrometer

    #mm
    xbin = 1
    xmin = -200
    xmax = 200

    sel = "is_spect==1"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    det = [{"nam": "up", "col": "red", "lab": "$x_{\mathrm{up}}$"}, {"nam": "down", "col": "blue", "lab": "$x_{\mathrm{down}}$"}]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    #leg.add_entry(leg_txt(), ltit[det])

    for i in det:

        hx = make_h1(inp, "event", i["nam"]+"_x", xbin, xmin, xmax, sel)
        plt.plot(hx[0], hx[1], "-", color=i["col"], lw=1)

        leg.add_entry(leg_lin(i["col"]), i["lab"])

    ax.set_xlabel("$x$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#x

#_____________________________________________________________________________
def y():

    #y position on spectrometer

    #mm
    xbin = 5
    xmin = -200
    xmax = 200

    sel = "is_spect==1"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    det = [{"nam": "up", "col": "red", "lab": "$y_{\mathrm{up}}$"}, {"nam": "down", "col": "blue", "lab": "$y_{\mathrm{down}}$"}]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    #leg.add_entry(leg_txt(), ltit[det])

    for i in det:

        hx = make_h1(inp, "event", i["nam"]+"_y", xbin, xmin, xmax, sel)
        plt.plot(hx[0], hx[1], "-", color=i["col"], lw=1)

        leg.add_entry(leg_lin(i["col"]), i["lab"])

    ax.set_xlabel("$y$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#y

#_____________________________________________________________________________
def theta_x():

    #theta_x angle at spectrometer

    #mrad
    xbin = 0.1
    #xmin = -20
    #xmax = 20
    xmin = -10
    xmax = 10

    sel = "is_spect==1"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    det = [{"nam": "up", "col": "red", "lab": r"$\theta_{x,\mathrm{up}}$"},\
      {"nam": "down", "col": "blue", "lab": r"$\theta_{x,\mathrm{down}}$"}]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    #leg.add_entry(leg_txt(), ltit[det])

    for i in det:

        hx = make_h1(inp, "event", i["nam"]+"_tx", xbin, xmin, xmax, sel)
        plt.plot(hx[0], hx[1], "-", color=i["col"], lw=1)

        leg.add_entry(leg_lin(i["col"]), i["lab"])

    ax.set_xlabel(r"$\theta_x$ (mrad)")
    ax.set_ylabel("Normalized counts")

    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#theta_x

#_____________________________________________________________________________
def theta_y():

    #theta_y angle at spectrometer

    #mrad
    xbin = 0.3
    xmin = -50
    xmax = 50

    sel = "is_spect==1"
    #sel += "&&up_calE>0.02"
    #sel += "&&down_calE>0.02"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    det = [{"nam": "up", "col": "red", "lab": r"$\theta_{y,\mathrm{up}}$"},\
      {"nam": "down", "col": "blue", "lab": r"$\theta_{y,\mathrm{down}}$"}]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    #leg.add_entry(leg_txt(), "theta_y")

    for i in det:

        hx = make_h1(inp, "event", i["nam"]+"_ty", xbin, xmin, xmax, sel)
        plt.plot(hx[0], hx[1], "-", color=i["col"], lw=1)

        leg.add_entry(leg_lin(i["col"]), i["lab"])

    ax.set_xlabel(r"$\theta_y$ (mrad)")
    ax.set_ylabel("Normalized counts")

    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#theta_y

#_____________________________________________________________________________
def calE():

    #calorimeter energy in spectrometer

    #GeV
    xbin = 0.01
    xmin = 0
    xmax = 1
    #xbin = 5e-4
    #xmin = 0
    #xmax = 0.06

    sel = "is_spect==1"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    det = [{"nam": "up", "col": "red"}, {"nam": "down", "col": "blue"}]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    #leg.add_entry(leg_txt(), ltit[det])

    for i in det:

        hx = make_h1(inp, "event", i["nam"]+"_calE", xbin, xmin, xmax, sel)
        plt.plot(hx[0], hx[1], "-", color=i["col"], lw=1)

    ax.set_xlabel("Calorimeter $E$ (GeV)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#calE

#_____________________________________________________________________________
def true_E():

    #true photon energy

    #GeV
    xbin = 0.1
    xmin = 0
    xmax = 19

    sel = "is_spect==1"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = make_h1(inp, "event", "true_phot_E", xbin, xmin, xmax, sel)
    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel("$E$ (GeV)")
    ax.set_ylabel("Normalized counts")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#true_E

#_____________________________________________________________________________
def true_pitheta():

    #true photon pi - theta in mrad

    #mrad
    xbin = 0.01
    xmin = 0
    xmax = 10

    sel = "is_spect==1"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = make_h1(inp, "event", "(TMath::Pi()-true_phot_theta)*1e3", xbin, xmin, xmax, sel)
    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel(r"$\pi - \theta$ (mrad)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#true_pitheta

#_____________________________________________________________________________
def true_phi():

    #true photon phi in rad

    #rad
    xbin = 0.01
    xmin = -3.5
    xmax = 3.5

    sel = "is_spect==1"

    #inp = "~/sim/lmon/analysis/ini/spect.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = make_h1(inp, "event", "true_phot_phi", xbin, xmin, xmax, sel)
    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel(r"$\phi$ (rad)")
    ax.set_ylabel("Normalized counts")

    #ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#true_phi

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



