#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 3

    func = {}
    func[0] = en
    func[1] = pitheta
    func[2] = phi
    func[3] = lQ2

    func[iplot]()

#_____________________________________________________________________________
def en():

    #GeV
    ebin = 0.1
    emin = 0
    emax = 20

    inp = "../../analysis/ini/tag_rec.root"

    #det = "s1"
    det = "s2"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get(det+"_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", ebin, emin, emax, ebin, emin, emax)

    tree.Draw("rec_el_E:true_el_E >> hxy", sel)

    hxy.SetXTitle("gen true E (GeV)")
    hxy.SetYTitle("rec E (GeV)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en

#_____________________________________________________________________________
def pitheta():

    #mrad
    tbin = 0.1
    tmin = 0
    tmax = 15

    inp = "../../analysis/ini/tag_rec.root"

    det = "s1"
    #det = "s2"

    #sel = "TMath::Pi()-rec_el_theta>0.001"
    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get(det+"_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", tbin, tmin, tmax, tbin, tmin, tmax)

    tree.Draw("(TMath::Pi()-rec_el_theta)*1e3:(TMath::Pi()-true_el_theta)*1e3 >> hxy", sel)

    hxy.SetXTitle("gen true pi-theta (mrad)")
    hxy.SetYTitle("rec pi-theta (mrad)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pitheta

#_____________________________________________________________________________
def phi():

    #GeV
    pbin = 0.1
    pmin = -TMath.Pi()-0.1
    pmax = TMath.Pi()+0.1

    inp = "../../analysis/ini/tag_rec.root"

    det = "s1"
    #det = "s2"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get(det+"_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", pbin, pmin, pmax, pbin, pmin, pmax)

    tree.Draw("rec_el_phi:true_el_phi >> hxy", sel)

    hxy.SetXTitle("gen true phi (rad)")
    hxy.SetYTitle("rec phi (rad)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phi

#_____________________________________________________________________________
def lQ2():

    #GeV
    qbin = 0.1
    qmin = -7
    qmax = -1

    inp = "../../analysis/ini/tag_rec.root"

    #det = "s1"
    det = "s2"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get(det+"_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", qbin, qmin, qmax, qbin, qmin, qmax)

    tree.Draw("TMath::Log10(rec_Q2):TMath::Log10(true_Q2) >> hxy", sel)

    hxy.SetXTitle("gen true log10(Q2) (GeV2)")
    hxy.SetYTitle("rec log10(Q2) (GeV2)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#lQ2









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




