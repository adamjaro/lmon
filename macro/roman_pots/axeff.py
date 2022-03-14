#!/usr/bin/python3

from ctypes import c_double, c_bool

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree
from ROOT import std

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2

    func = {}
    func[0] = acc_en_pitheta
    func[1] = eff_en_pitheta
    func[2] = acc_en

    func[iplot]()

#main

#_____________________________________________________________________________
def acc_en_pitheta():

    #2D acceptance in energy and pi - theta in mrad

    #inp = "../../analysis/ini/tag_rec.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4ax5/tag_rec_pass5.root"

    #tagger 1 or 2, both = 3
    tag = 3

    #bins in theta, mrad
    xbin = 0.2
    xmin = 0
    xmax = 12

    #bins in energy, GeV
    ybin = 0.3
    ymin = 1
    ymax = 20

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 1:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    elif tag == 2:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"
    elif tag == 3:
        sel = "s1_IsHit==1&&s2_IsHit==1"
        lab_sel = "Tagger 1 and 2"

    can = ut.box_canvas()

    hTag = ut.prepare_TH2D("hTag", xbin, xmin, xmax, ybin, ymin, ymax)
    hAll = ut.prepare_TH2D("hAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "true_el_E:(TMath::Pi()-true_el_theta)*1e3" # mrad
    tree.Draw(form+" >> hTag", sel)
    tree.Draw(form+" >> hAll")

    hTag.Divide(hAll)

    ytit = "Electron energy #it{E} (GeV)"
    xtit = "Electron polar angle #it{#pi}-#it{#theta} (mrad)"
    ut.put_yx_tit(hTag, ytit, xtit, 1.4, 1.3)

    hTag.SetTitleOffset(1.4, "Z")
    hTag.SetZTitle("Tagger acceptance")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hTag.SetMinimum(0)
    hTag.SetMaximum(1)
    hTag.SetContour(300)

    hTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_pitheta

#_____________________________________________________________________________
def eff_en_pitheta():

    #reconstruction efficiency in energy (GeV) and pi - theta (mrad)

    #inp = "../../analysis/ini/tag_rec.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4ax5/tag_rec_pass5.root"

    #tagger 1 or 2
    tag = 2

    #bins in theta, mrad
    xbin = 0.2
    xmin = 0
    xmax = 12

    #bins in energy, GeV
    ybin = 0.3
    ymin = 1
    ymax = 20

    infile = TFile.Open(inp)
    tree_in = infile.Get("event")

    tmp = TFile("tmp.root", "recreate")

    if tag == 1:
        sel = "s1_IsRec==1"
        lab_sel = "Tagger 1"
        tree = tree_in.CopyTree("s1_IsHit==1")
    else:
        sel = "s2_IsRec==1"
        lab_sel = "Tagger 2"
        tree = tree_in.CopyTree("s2_IsHit==1")

    can = ut.box_canvas()

    hTag = ut.prepare_TH2D("hTag", xbin, xmin, xmax, ybin, ymin, ymax)
    hAll = ut.prepare_TH2D("hAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "true_el_E:(TMath::Pi()-true_el_theta)*1e3" # mrad
    tree.Draw(form+" >> hTag", sel)
    tree.Draw(form+" >> hAll")

    hTag.Divide(hAll)

    ytit = "Electron energy #it{E} (GeV)"
    xtit = "Electron polar angle #it{#pi}-#it{#theta} (mrad)"
    ut.put_yx_tit(hTag, ytit, xtit, 1.4, 1.3)

    hTag.SetTitleOffset(1.4, "Z")
    hTag.SetZTitle("Reconstruction efficiency")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hTag.SetMinimum(0.)
    hTag.SetMaximum(1.)
    hTag.SetContour(300)

    hTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#eff_en_pitheta

#_____________________________________________________________________________
def acc_en():

    #energy acceptance or reconstruction efficiency

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag4ax5/tag_rec_pass5.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5a/tag_rec_pass5.root"

    emin = 0
    emax = 19

    amax = 1.1

    infile = TFile.Open(inp)
    tree_in = infile.Get("event")
    tree = tree_in

    as1 = rt.acc_Q2_kine(tree, "true_el_E", "s1_IsHit")
    as1.prec = 0.05
    as1.bmin = 0.1
    #as1.nev = int(1e4)
    #gs1 = as1.get()

    as2 = rt.acc_Q2_kine(tree, "true_el_E", "s2_IsHit")
    as2.prec = 0.6
    as2.bmin = 0.1
    #as2.nev = int(1e4)
    gs2 = as2.get()

    #lower scale for the plot
    amin = 999.
    #for i in (gs1, gs2):
    for i in (gs2,):
        print(i.GetName())
        for ip in range(i.GetN()):
            mm = 0.5*( i.GetPointY(ip) - i.GetErrorYlow(ip) )
            if mm < 1e-12:
                mm = 1e-12
            print("mm", mm)
            if mm < amin:
                amin = mm

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, amin, emax, amax)

    ut.put_yx_tit(frame, "Tagger acceptance", "Electron energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    #ut.set_graph(gs1, rt.kRed)
    #gs1.Draw("psame")

    ut.set_graph(gs2, rt.kBlue)
    gs2.Draw("psame")

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()














