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
    func[0] = chi2
    func[1] = xy
    func[2] = theta
    func[3] = ntrk
    func[4] = chi2_xy

    func[iplot]()

#_____________________________________________________________________________
def chi2():

    #chi^2/ndf for tracks, x and y separately, 2 degrees of freedom
    #for two tracks parameters and four measured points

    #chi^2
    #xbin = 1
    #xmax = 120
    xbin = 0.1
    xmax = 12

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    #sel = ""
    sel = "is_prim==1"

    hx = make_h1(inp, det, "chi2_x/2", xbin, 0, xmax, sel)
    hy = make_h1(inp, det, "chi2_y/2", xbin, 0, xmax, sel)

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
    plt.plot(hy[0], hy[1], "-", color="blue", lw=1)

    ax.set_xlabel("chi2/ndf")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#chi2

#_____________________________________________________________________________
def xy():

    #tracks position in xy

    #mm
    xybin = 1
    xymax = 80

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    #sel = ""
    sel = "(chi2_x<8)&&(chi2_y<8)&&(is_prim==0)"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    #tree.Print()

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("pos_y:pos_x >> hxy", sel)

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
def theta():

    #theta angle for tracks

    #mrad
    xbin = 1
    xmin = -100
    xmax = 100

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    #sel = ""
    #sel = "(chi2_x<8)&&(chi2_y<8)"
    sel = "(chi2_x<8)&&(chi2_y<8)&&(is_prim==1)"

    hx = make_h1(inp, det, "1e3*theta_x", xbin, xmin, xmax, sel)
    hy = make_h1(inp, det, "1e3*theta_y", xbin, xmin, xmax, sel)

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
    plt.plot(hy[0], hy[1], "-", color="blue", lw=1)

    ax.set_xlabel("theta (mrad)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#theta

#_____________________________________________________________________________
def ntrk():

    #number of tracks per event

    #tracks num
    xmax = 12

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v2.root"

    #det = "s1"
    det = "s2"
    #det = "s1_1"
    #det = "s2_1"

    val = "_ntrk"
    #val = "_nhit"

    hx = make_h1(inp, "event", det+val, 1, 0, xmax, det+val+">0")
    hy = make_h1(inp, "event", det+val+"_prim", 1, 0, xmax, det+val+"_prim>0")

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
    plt.plot(hy[0], hy[1], "-", color="blue", lw=1)

    ax.set_xlabel("Tracks per event")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#ntrk

#_____________________________________________________________________________
def chi2_xy():

    #tracks reduced chi^2 in x and y

    #mm
    #xybin = 1
    #xymax = 80
    xybin = 0.1
    xymax = 4

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    sel = ""
    #sel = "(chi2_x<8)&&(chi2_y<8)&&(is_prim==0)"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    #tree.Print()

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, 0, xymax, xybin, 0, xymax)

    tree.Draw("(chi2_y/2):(chi2_x/2) >> hxy", sel)

    hxy.SetXTitle("chi2 #it{x} (mm)")
    hxy.SetYTitle("chi2 #it{y} (mm)")

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

#chi2_xy

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax, sel=""):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)
    tree.Draw(val+" >> hx", sel)
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
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

