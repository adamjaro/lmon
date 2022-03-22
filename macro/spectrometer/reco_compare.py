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

    iplot = 0

    func = {}
    func[0] = en
    func[1] = pitheta
    func[2] = phi
    func[3] = eff_en_pitheta

    func[iplot]()

#_____________________________________________________________________________
def en():

    #GeV
    ebin = 0.1
    emin = 3
    emax = 19

    inp = "../../analysis/ini/spect_rec.root"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get("spec_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", ebin, emin, emax, ebin, emin, emax)

    tree.Draw("rec_E:true_phot_E >> hxy", sel)

    ytit = "Reconstructed energy #it{E_{e}} (GeV)"
    xtit = "Generated true energy #it{E_{e,gen}} (GeV)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

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
    tbin = 0.01
    tmin = 0
    tmax = 2

    inp = "../../analysis/ini/spect_rec.root"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get("spec_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", tbin, tmin, tmax, tbin, tmin, tmax)

    tree.Draw("(TMath::Pi()-rec_theta)*1e3:(TMath::Pi()-true_phot_theta)*1e3 >> hxy", sel)

    ytit = "Reconstructed #it{#pi-#theta_{#gamma}} (mrad)"
    xtit = "Generated true #it{#pi-#theta_{#gamma,gen}} (mrad)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

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

    inp = "../../analysis/ini/spect_rec.root"

    #sel = ""
    sel = "(TMath::Pi()-rec_theta)>0.8e-3"

    infile = TFile.Open(inp)
    tree = infile.Get("spec_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", pbin, pmin, pmax, pbin, pmin, pmax)

    tree.Draw("rec_phi:true_phot_phi >> hxy", sel)

    ytit = "Reconstructed #it{#phi_{#gamma}} (rad)"
    xtit = "Generated true #it{#phi_{#gamma,gen}} (rad)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.85, 0.24, 0.1, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#pi-#theta_{#it{e},rec} > 1 mrad", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phi

#_____________________________________________________________________________
def eff_en_pitheta():

    #reconstruction efficiency in energy (GeV) and pi - theta (mrad)

    inp = "../../analysis/ini/spect_rec.root"

    #bins in theta, mrad
    xbin = 0.01
    xmin = 0
    xmax = 2

    #bins in energy, GeV
    ybin = 0.3
    ymin = 1
    ymax = 20

    infile = TFile.Open(inp)
    tree_in = infile.Get("event")

    tmp = TFile("tmp.root", "recreate")
    tree = tree_in.CopyTree("is_spect==1")

    can = ut.box_canvas()

    hSpe = ut.prepare_TH2D("hSpe", xbin, xmin, xmax, ybin, ymin, ymax)
    hAll = ut.prepare_TH2D("hAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "true_phot_E:(TMath::Pi()-true_phot_theta)*1e3" # mrad
    tree.Draw(form+" >> hSpe", "is_rec==1")
    tree.Draw(form+" >> hAll")

    hSpe.Divide(hAll)

    ytit = "Photon energy #it{E} (GeV)"
    xtit = "Photon polar angle #it{#pi}-#it{#theta} (mrad)"
    ut.put_yx_tit(hSpe, ytit, xtit, 1.4, 1.3)

    hSpe.SetTitleOffset(1.4, "Z")
    hSpe.SetZTitle("Reconstruction efficiency")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hSpe.SetMinimum(0.)
    hSpe.SetMaximum(1.)
    hSpe.SetContour(300)

    hSpe.Draw("colz")

    #leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    #leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#eff_en_pitheta

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()






















