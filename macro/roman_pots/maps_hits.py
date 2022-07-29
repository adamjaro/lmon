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
    func[0] = xy
    func[1] = en
    func[2] = nhits
    func[3] = cls_size

    func[iplot]()

#_____________________________________________________________________________
def xy():

    #hits from pixels in xy

    #mm
    xybin = 1
    #xybin = 0.01
    #xymax = 220
    xymax = 90
    #xymax = 1

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5c/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v3.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx2/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic.root"

    det = "s1_4_clusters"
    #det = "s2A"

    sel = ""
    #sel = "is_prim==0"
    #sel = "id>2"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    #tree.Print()

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("y:x >> hxy", sel)
    #tree.Draw("(y+0.05):(x+0.05) >> hxy", sel)
    #tree.Draw("(y+0.1):(x+0.1) >> hxy", sel)

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
def en():

    #energy for hits or clusters

    #keV
    xbin = 1
    xmax = 500

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5c/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx1/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx2/maps_basic.root"

    #det = "s1_4_clusters"
    #det = "s2_4_clusters"
    #det = "s2C"

    #sel = ""
    #sel = "is_prim==0"

    val = "en"

    hx = make_h1(inp, "s1_4_clusters", val, xbin, 0, xmax)
    #hsel = make_h1(inp, det, val, xbin, 0, xmax, "is_prim==1")
    hy = make_h1(inp, "s2_4_clusters", val, xbin, 0, xmax)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(hx[0], hx[1], "-", color="blue", lw=1)
    #plt.plot(hsel[0], hsel[1], "-", color="red", lw=1)
    plt.plot(hy[0], hy[1], "-", color="red", lw=1)

    ax.set_xlabel("Cluster energy (keV)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    leg = legend()
    leg.add_entry(leg_lin("blue"), "Tagger 1, plane 4")
    leg.add_entry(leg_lin("red"), "Tagger 2, plane 4")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#en

#_____________________________________________________________________________
def nhits():

    #number of hits per event or cluster (depending on input)

    #keV
    xbin = 1
    xmax = 20

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx1/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx2/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic.root"

    #det = "event"
    #det = "s1_4_clusters"
    det = "s1_1_clusters"

    tnam = "Tagger 1, plane 1"
    #tnam = "Tagger 2, plane 4"

    #val = "s1_1_nhit"
    #val = "s1_4_ncls_prim"
    val = "nhits"

    #sel = ""
    #sel = "is_prim==1"
    #sel = val+">0"

    hx = make_h1(inp, det, val, xbin, 0, xmax)
    hsel = make_h1(inp, det, val, xbin, 0, xmax, "is_prim==1")

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(hx[0], hx[1], "-", color="blue", lw=1)
    plt.plot(hsel[0], hsel[1], "--", color="red", lw=1)

    ax.set_xlabel("Number of hits in cluster")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    leg = legend()
    leg.add_entry(leg_txt(), tnam)
    #leg.add_entry(leg_txt(), det)
    leg.add_entry(leg_lin("blue"), "All clusters")
    leg.add_entry(leg_lin("red", "--"), "Primary electrons")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#nhits

#_____________________________________________________________________________
def cls_size():

    #hits from pixels in xy

    #mm
    xbin = 0.005
    xmax = 0.1
    #xmax = 0.2

    #num of hits
    ybin = 1
    ymin = 1
    #ymax = 6
    ymax = 12

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx1/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx2/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v4.root"

    #det = "s1_4_clusters"
    det = "s1_1_clusters"

    #sel = ""
    sel = "nhits>1"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    #tree.Print()

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xbin, 0, xmax, ybin, ymin, ymax)

    #tree.Draw("nhits:sigma_x >> hxy", sel)
    tree.Draw("nhits:TMath::Sqrt(sigma_x*sigma_x+sigma_y*sigma_y) >> hxy", sel)

    hxy.SetXTitle("Cluster radius #sqrt{\sigma_{x}^{2} + \sigma_{y}^{2}} (mm)")
    hxy.SetYTitle("Number of hits in cluster")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.87, 0.24, 0.1, 0.035) # x, y, dx, dy, tsiz
    #tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "Tagger 1, plane 1", "")
    #leg.AddEntry("", det, "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#cls_size

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

