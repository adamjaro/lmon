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
    emin = 0
    emax = 18.5

    #mrad
    tmin = 0
    #tbin = 0.2
    #tmax = 300
    tbin = 0.2
    tmax = 12

    #log(GeV^2)
    lbin = 0.1
    lmin = -20
    lmax = 5

    inp = "/home/jaroslav/sim/GETaLM_data/qr/qr_18x275_T3p3_5Mevt.root"
    #inp = "/home/jaroslav/sim/GETaLM_data/py/pythia_ep_18x275_Q2all_T3p3_5Mevt.root"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    can = ut.box_canvas()

    hEQ2 = ut.prepare_TH3D("hE", ebin, emin, emax, tbin, tmin, tmax, lbin, lmin, lmax)

    tree.Draw("(TMath::Log10(true_Q2)):(TMath::Pi()-true_el_theta)*1e3:true_el_E >> hE", sel)

    hE = hEQ2.Project3DProfile("yx")

    hE.SetTitle("")
    ytit = "Polar angle #it{#pi-#theta_{e}} (mrad)"
    xtit = "Electron energy #it{E_{e}} (GeV)"
    ut.put_yx_tit(hE, ytit, xtit, 1.2, 1.2)

    hE.SetZTitle("Virtuality #it{Q}^{2} (GeV^{2})")
    hE.SetTitleOffset(1.7, "Z")

    ut.set_margin_lbtr(gPad, 0.09, 0.09, 0.02, 0.17)

    hE.SetMinimum(-7)
    hE.SetMaximum(-1)
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
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()







