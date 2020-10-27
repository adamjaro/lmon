#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1
    funclist = []
    funclist.append( make_all_E ) # 0
    funclist.append( make_qrpy ) # 1

    funclist[iplot]()

#main

#_____________________________________________________________________________
def make_qrpy():

    lqmin = -11
    lqmax = 5
    smax = 7.5

    basedir = "/home/jaroslav/sim/GETaLM_data"

    #sigma in micro barn

    gPy = make_sigma(basedir+"/py/pythia_ep_18x275_Q2all_beff2_5Mevt.root", 54.7)
    gQr = make_sigma(basedir+"/qr/qr_18x275_Qe_beff2_5Mevt.root", 54.8)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(lqmin, 0, lqmax, smax)
    frame.Draw()

    xtit = "log_{10}(#it{Q}^{2})"
    ytit = "#frac{d#it{#sigma}}{d("+xtit+")} (#mub/GeV^{2})"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.01, 0.01)

    gPy.SetLineColor(rt.kBlue)
    gQr.SetLineColor(rt.kRed)

    gQr.Draw("lsame")
    gPy.Draw("lsame")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(gPy, "Pythia6", "l")
    leg.AddEntry(gQr, "QR", "l")
    leg.Draw("same")

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#make_qrpy

#_____________________________________________________________________________
def make_all_E():

    lqmin = -11
    lqmax = 5
    smax = 7.5

    basedir = "/home/jaroslav/sim/lgen/data"

    #sigma in micro barn

    #g18x275 = make_sigma(basedir+"/lgen_18x275_qr_Qe_beff2_5Mevt.root", 55.1)
    #g10x100 = make_sigma(basedir+"/lgen_10x100_qr_5Mevt.root", 44.8)
    #g5x41 = make_sigma(basedir+"/lgen_5x41_qr_5Mevt.root", 33.4)

    g18x275 = make_sigma(basedir+"/lgen_py_18x275_Q2all_5Mevt.root", 54.7)
    g10x100 = make_sigma(basedir+"/lgen_py_10x100_Q2all_5Mevt.root", 40.9)
    g5x41 = make_sigma(basedir+"/lgen_py_5x41_Q2all_5Mevt.root", 28.4)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(lqmin, 0, lqmax, smax)
    frame.Draw()

    xtit = "log_{10}(#it{Q}^{2})"
    ytit = "#frac{d#it{#sigma}}{d("+xtit+")} (#mub/GeV^{2})"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.01, 0.01)

    g18x275.SetLineColor(rt.kRed)
    g10x100.SetLineColor(rt.kYellow+1)
    g5x41.SetLineColor(rt.kBlue)

    g18x275.Draw("lsame")
    g10x100.Draw("lsame")
    g5x41.Draw("lsame")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(g18x275, "18 #times 275 GeV", "l")
    leg.AddEntry(g10x100, "10 #times 100 GeV", "l")
    leg.AddEntry(g5x41, "5 #times 41 GeV", "l")
    leg.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#make_all_E

#_____________________________________________________________________________
def make_sigma(inp, sigma):

    lqbin = 0.2
    lqmin = -11
    lqmax = 5

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    hx = ut.prepare_TH1D("hx", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(true_Q2) >> hx")

    ut.norm_to_integral(hx, sigma)

    gx = ut.h1_to_graph(hx)
    #gx.SetLineColor(rt.kYellow+1)
    gx.SetLineWidth(3)

    return gx

#make_sigma

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")















