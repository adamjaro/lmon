#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import std

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = pitheta_en
    func[1] = lx_lQ2
    func[2] = lQ2

    func[iplot]()

#main

#_____________________________________________________________________________
def pitheta_en():

    #acceptance x efficiency in electron polar angle (y axis) and energy (x axis)

    #mrad
    ymin = 0
    ybin = 0.2
    ymax = 11

    #GeV
    xbin = 0.25
    xmin = 2
    xmax = 18.5

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v2.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx9/maps_basic_v2.root"

    #det = "s1"
    #det = "s2"

    #sel = "s1_is_sig_rec==1"
    #sel = "s2_is_sig_rec==1"
    sel = "s1_is_sig_rec==1 && s2_is_sig_rec==1"
    #sel = "s1_is_sig_rec==1 || s2_is_sig_rec==1"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    can = ut.box_canvas()

    hxy_all = ut.prepare_TH2D("hxy_all", xbin, xmin, xmax, ybin, ymin, ymax)
    hxy_sel = ut.prepare_TH2D("hxy_sel", xbin, xmin, xmax, ybin, ymin, ymax)

    val = "(TMath::Pi()-true_el_theta)*1e3:true_el_E"
    tree.Draw(val+" >> hxy_sel", sel)
    tree.Draw(val+" >> hxy_all")

    print("All: ", hxy_all.GetEntries())
    print("Sel: ", hxy_sel.GetEntries())
    print("AxE: ", hxy_sel.GetEntries()/hxy_all.GetEntries())

    hxy_sel.Divide(hxy_all)

    ytit = "Scattering (polar) angle #it{#pi-#theta_{e}} (mrad)"
    xtit = "Electron energy #it{E_{e}} (GeV)"
    ut.put_yx_tit(hxy_sel, ytit, xtit, 1.1, 1.2)

    hxy_sel.SetZTitle("Acceptance #times Efficiency #it{A}#times#it{E}")
    #hxy_sel.SetZTitle("Acceptance")
    hxy_sel.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.09, 0.09, 0.015, 0.15)

    gPad.SetGrid()

    hxy_sel.SetMinimum(0)
    hxy_sel.SetMaximum(1)
    hxy_sel.SetContour(300)

    hxy_sel.Draw("colz")

    leg = ut.prepare_leg(0.12, 0.88, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1": "Tagger 1", "s2": "Tagger 2"}
    #leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    #leg.AddEntry("", "Tagger 1 #bf{OR} Tagger 2", "")
    leg.AddEntry("", "Tagger 1 #bf{AND} Tagger 2", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pitheta_en

#_____________________________________________________________________________
def lx_lQ2():

    #acceptance x efficiency in Bjorken x and Q^2, both as log_10

    #log_10(x)
    ybin = 0.05
    ymin = -12
    ymax = -1

    #log_10(GeV^2)
    xbin = 0.05
    xmin = -9
    xmax = 0

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v2.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v2.root"

    #sel = "s1_is_sig_rec==1"
    #sel = "s2_is_sig_rec==1"
    #sel = "s1_is_sig_rec==1 && s2_is_sig_rec==1"
    sel = "s1_is_sig_rec==1 || s2_is_sig_rec==1"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    can = ut.box_canvas()

    hxy_all = ut.prepare_TH2D("hxy_all", xbin, xmin, xmax, ybin, ymin, ymax)
    hxy_sel = ut.prepare_TH2D("hxy_sel", xbin, xmin, xmax, ybin, ymin, ymax)

    val = "(TMath::Log10(true_x)):(TMath::Log10(true_Q2))"
    #tree.Draw(val+" >> hxy_sel", det+"_ntrk_prim>0")
    tree.Draw(val+" >> hxy_sel", sel)
    tree.Draw(val+" >> hxy_all")

    hxy_sel.Divide(hxy_all)

    ytit = "Bjorken #it{x}"
    xtit = "Virtuality #it{Q}^{2} (GeV^{2})"
    ut.put_yx_tit(hxy_sel, ytit, xtit, 1.4, 1.3)

    #hxy_sel.SetZTitle("Acceptance #times Efficiency #it{A}#times#it{E}")
    hxy_sel.SetZTitle("Acceptance")
    hxy_sel.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    gPad.SetGrid()

    hxy_sel.SetMinimum(0)
    hxy_sel.SetMaximum(1)
    hxy_sel.SetContour(300)

    #Q^2 labels in powers of 10
    ax = hxy_sel.GetXaxis()
    labels = range(-9, 1)
    for i in range(len(labels)):
        ax.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")
    ax.SetLabelOffset(0.015)

    #x labels in powers of 10
    ay = hxy_sel.GetYaxis()
    labels = range(-12, 0, 2)
    for i in range(len(labels)):
        ay.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")

    hxy_sel.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.88, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1": "Tagger 1", "s2": "Tagger 2"}
    #leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    #leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#lx_lQ2

#_____________________________________________________________________________
def lQ2():

    #acceptance x efficiency in Q^2

    #log_10(GeV^2)
    xbin = 0.05
    xmin = -9
    xmax = 0

    amin = 0
    amax = 0.3

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v2.root"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    axe = rt.acc_Q2_kine(tree, "true_Q2", "s1_is_sig_rec", "s2_is_sig_rec", 0)
    axe.modif = 1
    #axe.prec = 0.05
    #axe.bmin = 0.1
    axe.prec = 0.01
    axe.bmin = 0.08
    #axe.nev = int(1e4)
    gax = axe.get()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(xmin, amin, xmax, amax)

    ut.put_yx_tit(frame, "Acceptance", "Virtuality #it{Q}^{2} (GeV^{2})", 1.6, 1.5)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.11, 0.03, 0.03)

    gPad.SetGrid()

    ut.set_graph(gax, rt.kBlue)
    gax.Draw("psame")

    #Q^2 labels in powers of 10
    ax = frame.GetXaxis()
    labels = range(-9, 1)
    for i in range(len(labels)):
        ax.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")
    ax.SetLabelOffset(0.015)

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#lQ2

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()



















