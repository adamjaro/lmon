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
    func[0] = xy
    func[1] = theta_x
    func[2] = theta_y
    func[3] = true_el_E

    func[iplot]()

#_____________________________________________________________________________
def xy():

    #mm
    xybin = 1
    xymax = 80

    #inp = "../../analysis/ini/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag_pass2.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag4ax1/hits_tag_first10.root"

    #det = "s1"
    det = "s2"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("y:x >> hxy", sel)

    hxy.SetXTitle("#it{x} (mm)")
    hxy.SetYTitle("#it{y} (mm)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    hxy.GetXaxis().CenterTitle()
    hxy.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#xy

#_____________________________________________________________________________
def theta_x():

    #mrad
    tbin = 0.5
    tmin = -20
    tmax = 40

    #inp = "../../analysis/ini/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag_pass2.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag4ax1/hits_tag_first10.root"

    #det = "s1"
    det = "s2"

    val = "(theta_x*1e3)" # to mrad

    hx = make_h1(inp, det, val, tbin, tmin, tmax)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel("theta_x (mrad)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#theta_x

#_____________________________________________________________________________
def theta_y():

    #mrad
    tbin = 0.1
    tmin = -10
    tmax = 10
    #tmin = -5
    #tmax = -2.5

    #inp = "../../analysis/ini/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag_pass2.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag4ax1/hits_tag_first10.root"

    det = "s1"
    #det = "s2"

    val = "(theta_y*1e3)" # to mrad

    hx = make_h1(inp, det, val, tbin, tmin, tmax)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel("theta_y (mrad)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#theta_y

#_____________________________________________________________________________
def true_el_E():

    #GeV
    ebin = 0.5
    emax = 20

    inp = "../../analysis/ini/hits_tag.root"

    det = "s1"
    #det = "s2"

    val = "true_el_E"

    sel = "theta_x<0"

    hx = make_h1(inp, det, val, ebin, 0, emax, sel)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    ax.set_xlabel("energy (GeV)")
    ax.set_ylabel("Normalized counts")

    #ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#true_el_E

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax, sel=""):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)
    tree.Draw(val+" >> hx", sel)
    #ut.norm_to_integral(hx, 1.)

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


