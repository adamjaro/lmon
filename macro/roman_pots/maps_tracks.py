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
    func[5] = tx_en

    func[iplot]()

#_____________________________________________________________________________
def chi2():

    #chi^2/ndf for tracks, x and y separately, 2 degrees of freedom
    #for two tracks parameters and four measured points

    #chi^2
    #xbin = 1
    #xmax = 120
    xbin = 0.05
    xmax = 12

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx1/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx2/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v5.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    sel = ""
    #sel = "is_prim==1"
    #sel = "is_prim==0"
    #sel = "is_associate==1"

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

    ax.set_xlabel("Tracks $\chi^2$/ndf")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    leg = legend()
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.add_entry(leg_txt(), tnam[det])
    if sel == "":
        leg.add_entry(leg_txt(), "All tracks")
    elif sel == "is_prim==1":
        leg.add_entry(leg_txt(), "Primary electrons")
    else:
        leg.add_entry(leg_txt(), sel)

    leg.add_entry(leg_lin("red"), "$\chi^2_x$/ndf (horizontal)")
    leg.add_entry(leg_lin("blue"), "$\chi^2_y$/ndf (vertical)")
    leg.draw(plt, col)

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
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx1/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    sel = ""
    #sel = "(chi2_x<8)&&(chi2_y<8)&&(is_prim==0)"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    #tree.Print()

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("pos_y:pos_x >> hxy", sel)

    hxy.SetXTitle("#it{x_{0}} (mm)")
    hxy.SetYTitle("#it{y_{0}} (mm)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    hxy.GetXaxis().CenterTitle()
    hxy.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#xy

#_____________________________________________________________________________
def theta():

    #theta angle for tracks

    #mrad
    xbin = 1
    xmin = -100
    xmax = 100
    #xbin = 0.4
    #xmin = -4
    #xmax = 6

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx1/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx2/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic.root"

    det = "s1_tracks"
    #det = "s2_tracks"

    #val = "theta_x"
    val = "theta_y"

    hx = make_h1(inp, det, "1e3*"+val, xbin, xmin, xmax)
    hsel = make_h1(inp, det, "1e3*"+val, xbin, xmin, xmax, "is_prim==1")


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

    tnam = {"theta_x": r"$\theta_x$", "theta_y": r"$\theta_y$"}
    ax.set_xlabel(tnam[val]+" (mrad)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    leg = legend()
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.add_entry(leg_txt(), tnam[det])
    leg.add_entry(leg_lin("blue"), "All tracks")
    leg.add_entry(leg_lin("red", "--"), "Primary electrons")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#theta

#_____________________________________________________________________________
def ntrk():

    #number of tracks per event

    #tracks num
    #xmax = 30
    xmax = 400

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx1/maps_basic.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx2/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v5.root"

    #det = "s1"
    det = "s2"
    #det = "cnt_s1"
    #det = "cnt_s2"

    val = "_ntrk"
    #val = "_nhit"

    hx = make_h1(inp, "event", det+val, 1, 0, xmax, det+val+">0")
    hy = make_h1(inp, "event", det+val+"_prim", 1, 0, xmax, det+val+"_prim>0")
    hy1 = make_h1(inp, "event", det+val+"_associate", 1, 0, xmax, det+val+"_associate>0")

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
    plt.plot(hy[0], hy[1], "--", color="red", lw=1)
    plt.plot(hy1[0], hy1[1], "--", color="gold", lw=1)

    ax.set_xlabel("Tracks per event")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    leg = legend()
    #tnam = {"s1": "Tagger 1", "s2": "Tagger 2"}
    #leg.add_entry(leg_txt(), tnam[det])
    leg.add_entry(leg_txt(), det)
    leg.add_entry(leg_lin("blue"), "All tracks")
    leg.add_entry(leg_lin("red", "--"), "Primary electrons")
    leg.draw(plt, col)

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
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v5.root"

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
def tx_en():

    #theta_x and energy for tagger 1 to address peak in theta_x below 0

    #mrad
    xbin = 0.4
    xmin = -4
    xmax = 7

    #GeV
    ybin = 0.3
    ymin = 4
    ymax = 20

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5d/maps_basic_v6.root"

    det = "s1_tracks"

    #sel = ""
    sel = "is_prim==1"
    #sel = "id>2"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    #tree.Print()

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("(true_el_E):(theta_x*1e3) >> hxy", sel)

    hxy.SetXTitle("#it{#theta_{x}} (mrad)")
    hxy.SetYTitle("True electron energy (GeV)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    #hxy.GetXaxis().CenterTitle()
    #hxy.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#tx_en

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax, sel=""):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)
    tree.Draw(val+" >> hx", sel)
    print("Entries:", hx.GetEntries())
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

