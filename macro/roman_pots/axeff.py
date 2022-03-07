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

    iplot = 1

    func = {}
    func[0] = acc_en_pitheta
    func[1] = eff_en_pitheta

    func[iplot]()

#main

#_____________________________________________________________________________
def acc_en_pitheta():

    #2D acceptance in energy and pi - theta in mrad

    inp = "../../analysis/ini/tag_rec.root"

    #bins in theta, mrad
    xbin = 0.2
    xmin = 0
    xmax = 12

    #bins in energy, GeV
    ybin = 0.3
    ymin = 1
    ymax = 20

    #tagger 1 or 2
    tag = 1

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 1:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

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

    inp = "../../analysis/ini/tag_rec.root"

    #bins in theta, mrad
    xbin = 0.2
    xmin = 0
    xmax = 12

    #bins in energy, GeV
    ybin = 0.3
    ymin = 1
    ymax = 20

    #tagger 1 or 2
    tag = 2

    infile = TFile.Open(inp)
    tree_in = infile.Get("event")

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

    hTag.SetMinimum(0)
    hTag.SetMaximum(1)
    hTag.SetContour(300)

    hTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#eff_en_pitheta

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    #gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()


