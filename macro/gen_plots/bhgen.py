#!/usr/bin/python3

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 4

    funclist = {}
    funclist[0] = en_pT
    funclist[1] = pitheta_pT
    funclist[2] = pitheta_en
    funclist[3] = eltheta_pT
    funclist[4] = theta_both

    funclist[iplot]()

#main

#_____________________________________________________________________________
def en_pT():

    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5/evt.root"
    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    inp = "/home/jaroslav/sim/bhgen/data/g10x100_emin0p5_100Mevt/evt.root"

    #proton pT, MeV
    xbin = 2
    xmin = 0
    xmax = 200

    #photon energy, GeV
    ybin = 0.2
    ymin = 0.1
    #ymax = 19
    ymax = 11

    infile = TFile.Open(inp)
    tree = infile.Get("bhgen_tree")

    can = ut.box_canvas()

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("phot_en:(p_pt*1e3) >> hXY")

    ytit = "Photon energy #it{E}_{#gamma} (GeV)"
    xtit = "Proton #it{p}_{T} (MeV)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.3, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.11)

    gPad.SetGrid()
    gPad.SetLogz()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw("colz")

    leg = ut.prepare_leg(0.5, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry("", "18x275 GeV", "")
    leg.AddEntry("", "10x100 GeV", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_pT

#_____________________________________________________________________________
def pitheta_pT():

    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5/evt.root"
    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    inp = "/home/jaroslav/sim/bhgen/data/g10x100_emin0p5_100Mevt/evt.root"

    #proton pT, MeV
    xbin = 2
    xmin = 0
    xmax = 200

    #photon scattering angle as pi - theta, mrad
    ybin = 0.1
    ymin = 0
    ymax = 12

    infile = TFile.Open(inp)
    tree = infile.Get("bhgen_tree")

    can = ut.box_canvas()

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("((TMath::Pi()-phot_theta)*1000):(p_pt*1e3) >> hXY")

    ytit = "Photon scattering angle #it{#pi}-#it{#theta}_{#gamma} (mrad)"
    xtit = "Proton #it{p}_{T} (MeV)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.3, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.11)

    gPad.SetGrid()
    gPad.SetLogz()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw("colz")

    leg = ut.prepare_leg(0.5, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry("", "18x275 GeV", "")
    leg.AddEntry("", "10x100 GeV", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pitheta_pT

#_____________________________________________________________________________
def pitheta_en():

    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5/evt.root"
    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    inp = "/home/jaroslav/sim/bhgen/data/g10x100_emin0p5_100Mevt/evt.root"

    #photon energy, GeV
    xbin = 0.3
    xmin = 0.1
    #xmax = 19
    xmax = 11

    #photon scattering angle as pi - theta, mrad
    ybin = 0.2
    ymin = 0
    ymax = 12

    infile = TFile.Open(inp)
    tree = infile.Get("bhgen_tree")

    can = ut.box_canvas()

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("((TMath::Pi()-phot_theta)*1000):phot_en >> hXY", "p_pt*1e3 > 50")#, "", int(5e6))

    ytit = "Photon scattering angle #it{#pi}-#it{#theta}_{#gamma} (mrad)"
    xtit = "Photon energy #it{E}_{#gamma} (GeV)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.3, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.11)

    gPad.SetGrid()
    gPad.SetLogz()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw("colz")

    leg = ut.prepare_leg(0.5, 0.85, 0.24, 0.1, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry("", "18x275 GeV", "")
    leg.AddEntry("", "10x100 GeV", "")
    leg.AddEntry("", "Proton #it{p}_{T} > 50 MeV", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pitheta_en

#_____________________________________________________________________________
def eltheta_pT():

    inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5/evt.root"
    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    #inp = "/home/jaroslav/sim/bhgen/data/g10x100_emin0p5_100Mevt/evt.root"

    #proton pT, MeV
    xbin = 2
    xmin = 0
    xmax = 200

    #electron scattering angle as pi - theta_e, mrad
    ybin = 0.6
    ymin = 0
    ymax = 30

    infile = TFile.Open(inp)
    tree = infile.Get("bhgen_tree")

    can = ut.box_canvas()

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("((TMath::Pi()-el_theta)*1000):(p_pt*1e3) >> hXY")

    ytit = "Electron scattering angle #it{#pi}-#it{#theta}_{e} (mrad)"
    xtit = "Proton #it{p}_{T} (MeV)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.3, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.11)

    gPad.SetGrid()
    gPad.SetLogz()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw("colz")

    leg = ut.prepare_leg(0.5, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "18x275 GeV", "")
    #leg.AddEntry("", "10x100 GeV", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#eltheta_pT

#_____________________________________________________________________________
def theta_both():

    #inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5/evt.root"
    inp = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    #inp = "/home/jaroslav/sim/bhgen/data/g10x100_emin0p5_100Mevt/evt.root"

    #photon scattering angle as pi - theta, mrad
    xbin = 0.2
    xmin = 0
    xmax = 12

    #electron scattering angle as pi - theta_e, mrad
    ybin = 0.6
    ymin = 0
    ymax = 30

    infile = TFile.Open(inp)
    tree = infile.Get("bhgen_tree")

    can = ut.box_canvas()

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    sel = "(p_pt*1e3>50)&&(el_en>8)&&(el_en<16)&&(phot_en>5)"
    tree.Draw("((TMath::Pi()-el_theta)*1000):((TMath::Pi()-phot_theta)*1000) >> hXY", sel)

    ytit = "Electron scattering angle #it{#pi}-#it{#theta}_{e} (mrad)"
    xtit = "Photon scattering angle #it{#pi}-#it{#theta}_{#gamma} (mrad)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.3, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.11)

    gPad.SetGrid()
    gPad.SetLogz()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw("colz")

    leg = ut.prepare_leg(0.45, 0.75, 0.24, 0.2, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "18x275 GeV", "")
    #leg.AddEntry("", "10x100 GeV", "")
    leg.AddEntry("", "Proton #it{p}_{T} > 50 MeV", "")
    leg.AddEntry("", "Electron 8 < #it{E}_{e} < 16 GeV", "")
    leg.AddEntry("", "Photon #it{E}_{#gamma} > 5 GeV", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#eltheta_pT

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()








