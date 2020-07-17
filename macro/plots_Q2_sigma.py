#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile

import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2
    funclist = []
    funclist.append( make_qr ) # 0
    funclist.append( make_py ) # 1
    funclist.append( make_both ) # 2

    funclist[iplot]()

#_____________________________________________________________________________
def make_qr():

    #quasi-real total cross section
    #sigma_qr = 53.839868617 # micro barn
    #infile = "../data/lmon_18x275_qr_Qd_beff2_5Mevt.root"
    sigma_qr = 55.1027755249 # micro barn
    infile = "../../lgen/data/lgen_18x275_qr_Qe_beff2_5Mevt.root"

    lqbin = 0.2
    lqmin = -11
    lqmax = 5

    inp = TFile.Open(infile)
    #tree = inp.Get("DetectorTree")
    tree = inp.Get("ltree")

    #can = ut.box_canvas()

    hQ2 = ut.prepare_TH1D("hQ2", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(true_Q2) >> hQ2")

    ut.norm_to_integral(hQ2, sigma_qr)

    gQr = ut.h1_to_graph(hQ2)
    gQr.SetLineColor(rt.kRed)
    gQr.SetLineWidth(3)

    return gQr

    hQ2.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")


#_____________________________________________________________________________
def make_py():

    #Pythia6 total cross section
    sigma_py = 54.700142803416348 # micro barn
    infile = "../data/lmon_py_18x275_Q2all_beff2_5Mevt.root"

    lqbin = 0.2
    lqmin = -11
    lqmax = 5

    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #can = ut.box_canvas()

    hQ2 = ut.prepare_TH1D("hQ2", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(true_Q2) >> hQ2")

    ut.norm_to_integral(hQ2, sigma_py)

    gPy = ut.h1_to_graph(hQ2)
    gPy.SetLineColor(rt.kRed)
    gPy.SetLineWidth(3)
    gPy.SetLineStyle(rt.kDashed)

    return gPy

    #print hQ2.Integral("width")

    hQ2.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def make_both():

    lqmin = -11
    lqmax = 5
    ymax = 8.5

    gQr = make_qr()
    gPy = make_py()
    gQr10x100 = make_qr_10x100()
    gQr5x41 = make_qr_5x41()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(lqmin, 0, lqmax, ymax)
    frame.Draw()

    xtit = "log_{10}(#it{Q}^{2})"
    ytit = "#frac{d#it{#sigma}}{d("+xtit+")} (#mub/GeV^{2})"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.02)

    gQr.Draw("lsame")
    gPy.Draw("lsame")
    gQr10x100.Draw("lsame")
    gQr5x41.Draw("lsame")

    leg = ut.prepare_leg(0.53, 0.83, 0.2, 0.1, 0.035)
    leg.AddEntry(gPy, "Pythia6", "l")
    leg.AddEntry(gQr, "Quasi-real photoproduction", "l")
    leg.AddEntry(gQr10x100, "Quasi-real 10x100", "l")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def make_qr_10x100():

    #quasi-real total cross section for 10x100 beams

    sigma_qr = 56.3121075698 # micro barn
    infile = "../../lgen/data/lgen_10x100_qr_Qe_5Mevt.root"

    lqbin = 0.2
    lqmin = -11
    lqmax = 5

    inp = TFile.Open(infile)
    tree = inp.Get("ltree")

    hQ2 = ut.prepare_TH1D("hQ2", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(true_Q2) >> hQ2")

    ut.norm_to_integral(hQ2, sigma_qr)

    gQr = ut.h1_to_graph(hQ2)
    gQr.SetLineColor(rt.kYellow+1)
    gQr.SetLineWidth(3)

    return gQr

#_____________________________________________________________________________
def make_qr_5x41():

    #quasi-real total cross section for 5x41 beams

    sigma_qr = 65.0648514567 # micro barn
    infile = "../../lgen/data/lgen_5x41_qr_Qe_5Mevt.root"

    lqbin = 0.2
    lqmin = -11
    lqmax = 5

    inp = TFile.Open(infile)
    tree = inp.Get("ltree")

    hQ2 = ut.prepare_TH1D("hQ2", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(true_Q2) >> hQ2")

    ut.norm_to_integral(hQ2, sigma_qr)

    gQr = ut.h1_to_graph(hQ2)
    gQr.SetLineColor(rt.kBlue)
    gQr.SetLineWidth(3)

    return gQr

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()


