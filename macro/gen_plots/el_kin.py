#!/usr/bin/python3

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    funclist = {}
    funclist[0] = en_pitheta
    funclist[1] = en_pitheta_lQ2
    funclist[2] = lx_lQ2_en
    funclist[3] = true_lQ2_el_lQ2
    funclist[iplot]()

#main

#_____________________________________________________________________________
def en_pitheta():

    #electron energy and pi-theta angle

    #GeV
    ebin = 0.01
    emin = 17
    emax = 19

    #mrad
    tbin = 0.1
    tmin = 0
    tmax = 500

    inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_18x275_T3p3_5Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/py/pythia_ep_18x275_Q2all_T3p3_5Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/lumi/lumi_18x275_Lif_emin0p5_T3p3_10Mevt_v2.root"

    sel = ""
    #sel = "true_el_E>18"
    #sel = "(true_el_E>17.9)&&((TMath::Pi()-true_el_theta)*1e3<30)"

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    #tree.Print()
    #return

    can = ut.box_canvas()

    hE = ut.prepare_TH2D("hE", ebin, emin, emax, tbin, tmin, tmax)

    tree.Draw("(TMath::Pi()-true_el_theta)*1e3:true_el_E >> hE", sel)

    print("Entries:", hE.GetEntries())

    ytit = "pi-theta (mrad)"
    xtit = "E (GeV)"
    ut.put_yx_tit(hE, ytit, xtit, 1.6, 1.4)

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.13)

    hE.SetMinimum(0.98)
    hE.SetContour(300)

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_pitheta

#_____________________________________________________________________________
def en_pitheta_lQ2():

    #electron energy, pi-theta angle and log10(Q^2) as color scale

    #GeV
    #ebin = 0.02
    #emin = 17
    #emax = 19
    ebin = 0.2
    #ebin = 0.09
    emin = 0
    emax = 18.5
    #emax = 5.02

    #mrad
    tmin = 0
    #tmax = 300
    tbin = 0.2
    #tbin = 0.8
    tmax = 12
    #tmax = 99

    #log(GeV^2)
    lbin = 0.1
    lmin = -20
    lmax = 5

    #inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_18x275_T3p3_5Mevt.root"
    inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_bx_18x275_T3p3_10Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_5x41_T3p3_10Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/py/pythia_ep_18x275_Q2all_T3p3_5Mevt.root"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    can = ut.box_canvas()

    hEQ2 = ut.prepare_TH3D("hE", ebin, emin, emax, tbin, tmin, tmax, lbin, lmin, lmax)

    tree.Draw("(TMath::Log10(true_Q2)):(TMath::Pi()-true_el_theta)*1e3:true_el_E >> hE", sel)

    hE = hEQ2.Project3DProfile("yx")

    hE.SetTitle("")
    ytit = "Scattering (polar) angle #it{#pi-#theta_{e}} (mrad)"
    xtit = "Electron energy #it{E_{e}} (GeV)"
    ut.put_yx_tit(hE, ytit, xtit, 1.1, 1.2)

    hE.SetZTitle("Virtuality #it{Q}^{2} (GeV^{2})")
    hE.SetTitleOffset(1.7, "Z")

    ut.set_margin_lbtr(gPad, 0.09, 0.09, 0.02, 0.17)

    hE.SetMinimum(-7)
    hE.SetMaximum(-1)
    #hE.SetMaximum(-0.4)
    hE.SetContour(300)

    #Q^2 labels in powers of 10
    az = hE.GetZaxis()
    labels = range(-7, 0)
    for i in range(len(labels)):
        az.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")

    gPad.SetGrid()

    hE.Draw("colz")

    #gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_pitheta_lQ2

#_____________________________________________________________________________
def lx_lQ2_en():

    #log_10(x) (y axis), log_10(Q^2) (x axis) and electron energy as color scale

    #log_10(x), y axis
    ybin = 0.05
    ymin = -12
    ymax = -1

    #log_10(GeV^2), x axis
    xbin = 0.05
    xmin = -9
    xmax = 0

    #GeV, z axis as color scale
    zbin = 0.05
    zmin = 0
    zmax = 18
    #zmin = 0.0001
    #zmax = 1.26

    inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_18x275_T3p3_5Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/py/pythia_ep_18x275_Q2all_T3p3_5Mevt.root"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    can = ut.box_canvas()

    hxyz = ut.prepare_TH3D("hxyz", xbin, xmin, xmax, ybin, ymin, ymax, zbin, zmin, zmax)

    tree.Draw("true_el_E:(TMath::Log10(true_x)):(TMath::Log10(true_Q2)) >> hxyz", sel) # zyx

    hxy = hxyz.Project3DProfile("yx")

    hxy.SetTitle("")
    ytit = "Bjorken #it{x}"
    xtit = "Virtuality #it{Q}^{2} (GeV^{2})"
    ut.put_yx_tit(hxy, ytit, xtit, 1.4, 1.3)

    hxy.SetZTitle("Electron energy #it{E_{e}} (GeV)")
    hxy.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    hxy.SetMinimum(0)
    hxy.SetMaximum(18)
    hxy.SetContour(300)

    #Q^2 labels in powers of 10
    ax = hxy.GetXaxis()
    labels = range(-9, 1)
    for i in range(len(labels)):
        ax.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")
    ax.SetLabelOffset(0.015)

    #x labels in powers of 10
    ay = hxy.GetYaxis()
    labels = range(-12, 0, 2)
    for i in range(len(labels)):
        ay.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")

    gPad.SetGrid()

    hxy.Draw("colz")

    #gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#lx_lQ2_en

#_____________________________________________________________________________
def true_lQ2_el_lQ2():

    #electron Q^2 (y axis) and true Q^2 (x axis), both as log_10
    #according to GETaLM paper plot in plot_TrueQ2elQ2.py

    basedir = ""

    inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_5x41_T3p3_10Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_18x275_T3p3_5Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_bx_18x275_T3p3_10Mevt.root"

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    #tree.Print()
    #return

    lqbin = 0.08
    #lqbin = 0.03
    lqmin = -10
    lqmax = 4.5

    hQ2 = ut.prepare_TH2D("hQ2", lqbin, lqmin, lqmax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    #gStyle.SetPalette(56)

    #Q2form = "(2*18*el_en*(1-TMath::Cos(TMath::Pi()-el_theta)))"
    Q2form = "(2*5*el_en*(1-TMath::Cos(TMath::Pi()-el_theta)))"

    tree.Draw("TMath::Log10("+Q2form+"):TMath::Log10(true_Q2) >> hQ2")

    ytit = "Electron  log_{10}(#it{Q}^{2}_{e})"#+" / {0:.3f}".format(xbin)
    xtit = "Generator true  log_{10}(#it{Q}^{2})"#+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hQ2, ytit, xtit, 1.6, 1.4)

    ut.set_margin_lbtr(gPad, 0.12, 0.11, 0.03, 0.12)

    hQ2.Draw()

    hQ2.SetMinimum(0.98)
    hQ2.SetContour(300)

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#true_lQ2_el_lQ2

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()







