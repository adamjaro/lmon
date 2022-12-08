#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2

    func = {}
    func[0] = make_all_E
    func[1] = make_qrpy
    func[2] = sigma_en
    func[3] = sigma_pitheta

    func[iplot]()

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
def sigma_en():

    #cross section as a function of electron energy

    emin = 0 # GeV
    emax = 23
    smin = 1e-4
    smax = 1e3 # mb
    #smax = 1 # mb

    ebin = 0.2

    basedir = "/home/jaroslav/sim/GETaLM_data"

    g1 = make_sigma(basedir+"/lumi/lumi_18x275_Lif_emin0p5_T3p3_10Mevt.root", "true_el_E", 0.1, emin, emax, 171.3)
    g2 = make_sigma(basedir+"/qr/qr_18x275_T3p3_5Mevt.root", "true_el_E", ebin, emin, emax, 0.053)
    #g3 = make_sigma(basedir+"/py/pythia_ep_18x275_Q2all_beff2_5Mevt.root", "true_el_E", ebin, emin, emax, 0.055)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, smin, emax, smax)
    frame.Draw()

    xtit = "Electron energy #it{E_{e}} (GeV)"
    ytit = "#frac{d#it{#sigma}}{d#it{E_{e}}} (mb/GeV)"
    ut.put_yx_tit(frame, ytit, xtit, 1.7, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.02)

    g1.SetLineColor(rt.kBlue) # kBlue
    g2.SetLineColor(rt.kRed) # kRed
    #g3.SetLineColor(rt.kGreen+1) # kGreen+1
    g2.SetLineStyle(rt.kDashed)

    g1.Draw("lsame")
    #g3.Draw("lsame")
    g2.Draw("lsame")

    gPad.SetLogy()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.2, 0.8, 0.24, 0.15, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(g1, "Bremsstrahlung", "l")
    leg.AddEntry(g2, "Quasi-real photoproduction", "l")
    #leg.AddEntry(g3, "Pythia6", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#sigma_en

#_____________________________________________________________________________
def sigma_pitheta():

    #cross section as a function of electron scattering angle as pi - theta in mrad

    tmin = 0 # mrad
    tmax = 25
    smin = 1e-4
    smax = 2e3 # mb

    basedir = "/home/jaroslav/sim/GETaLM_data"

    form = "(TMath::Pi()-true_el_theta)*1e3"

    g1 = make_sigma_2(basedir+"/lumi/lumi_18x275_Lif_emin0p5_T3p3_10Mevt.root", form, 0.2, tmin, tmax, 171.3, 5, 1.2)
    g2 = make_sigma(basedir+"/qr/qr_18x275_T3p3_5Mevt.root", form, 0.2, tmin, tmax, 0.053)
    g3 = make_sigma(basedir+"/py/pythia_ep_18x275_Q2all_beff2_5Mevt.root", form, 0.2, tmin, tmax, 0.055)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(tmin, smin, tmax, smax)
    frame.Draw()

    xtit = "#it{#pi - #theta_{e}}' (mrad)"
    ytit = "#frac{d#it{#sigma}}{d#it{#theta_{e}}'} (mb/mrad)"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.02)
    g1.SetLineColor(rt.kBlue)
    g2.SetLineColor(rt.kRed)
    g3.SetLineColor(rt.kGreen+1)
    g3.SetLineStyle(rt.kDashed)

    g1.Draw("lsame")
    g2.Draw("lsame")
    g3.Draw("lsame")

    leg = ut.prepare_leg(0.6, 0.75, 0.24, 0.15, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(g1, "Bremsstrahlung", "l")
    leg.AddEntry(g2, "Quasi-real", "l")
    leg.AddEntry(g3, "Pythia6", "l")
    leg.Draw("same")

    gPad.SetLogy()

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#sigma_pitheta

#_____________________________________________________________________________
def make_sigma(inp, plot, xbin, xmin ,xmax, sigma, tnam="ltree"):

    #cross section plot from the tree

    infile = TFile.Open(inp)
    tree = infile.Get(tnam)

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)

    tree.Draw(plot+" >> hx")

    ut.norm_to_integral(hx, sigma)

    #gx = ut.h1_to_graph(hx)
    gx = ut.h1_to_graph_nz(hx, 1e-5)
    gx.SetLineWidth(3)

    return gx

#make_sigma

#_____________________________________________________________________________
def make_sigma_2(inp, plot, xbin, xmin, xmax, sigma, xmid, bin2):

    #cross section in two binning intervals from the tree

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    #point to start longer bins
    #xmid = 1
    #bin2 = xbin*10.  #  4.
    #xmid = 1.1
    #bin2 = xbin*6.

    hx = ut.prepare_TH1D_vec("hx", ut.get_bins_vec_2pt(xbin, bin2, xmin, xmax, xmid))

    tree.Draw(plot+" >> hx")

    #normalize to the width of each bin, necessary for variable binning
    for ibin in range(hx.GetNbinsX()+1):
        hx.SetBinContent(ibin, hx.GetBinContent(ibin)/hx.GetBinWidth(ibin))

    ut.norm_to_integral(hx, sigma)

    gx = ut.h1_to_graph(hx)
    gx.SetLineWidth(3)

    return gx

#make_sigma_2

#_____________________________________________________________________________
#def make_sigma(inp, sigma):

#    lqbin = 0.2
#    lqmin = -11
#    lqmax = 5

#    infile = TFile.Open(inp)
#    tree = infile.Get("ltree")

#    hx = ut.prepare_TH1D("hx", lqbin, lqmin, lqmax)

#    tree.Draw("TMath::Log10(true_Q2) >> hx")

#    ut.norm_to_integral(hx, sigma)

#    gx = ut.h1_to_graph(hx)
#    #gx.SetLineColor(rt.kYellow+1)
#    gx.SetLineWidth(3)

#    return gx

#make_sigma

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")















