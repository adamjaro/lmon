#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2
    funclist = []
    funclist.append( make_theta_allE ) # 0
    funclist.append( make_sig_E ) # 1
    funclist.append( make_E_theta ) # 2

    funclist[iplot]()

#main

#_____________________________________________________________________________
def make_theta_allE():

    #theta for all beam energies

    tmin = 0
    tmax = 5
    tbin = 0.03 #  0.05
    smax = 3e7  #  1e4
    smin = 1e-3 #  1e-2

    gdir = "/home/jaroslav/sim/GETaLM_data/lumi/"

    #inE1 = ["lumi_18x275_Lif_emin0p1_1Mevt.root", 276.35]
    #inE2 = ["lumi_10x100_Lif_emin0p1_1Mevt.root", 217.09]
    #inE3 = ["lumi_5x41_Lif_emin0p1_1Mevt.root", 159.33]

    #inE1 = ["lumi_18x275_Lif_emin0p5_beff2_5Mevt.root", 171.29]
    inE1 = ["lumi_18x275_Lif_emin0p5_d200_beff3_5Mevt.root", 171.29]
    #inE2 = ["lumi_10x100_Lif_emin0p5_beff2_5Mevt.root", 123.83]
    inE2 = ["lumi_10x100_Lif_emin0p5_beff3_5Mevt.root", 123.83]
    #inE3 = ["lumi_5x41_Lif_emin0p5_beff2_5Mevt.root", 79.18]
    inE3 = ["lumi_5x41_Lif_emin0p5_beff3_5Mevt.root", 79.18]
    #inE4 = ["lumi_eAu_18x110_Lif_emin0p5_beff2_5Mevt.root", 963626.6]
    inE4 = ["lumi_eAu_18x110_Lif_emin0p5_d200_beff2_5Mevt.root", 963626.6]
    inE5 = ["lumi_eAu_5x41_Lif_emin0p5_beff2_5Mevt.root", 462904.4]

    plot = "(TMath::Pi()-phot_theta)*1000"
    #plot = "(TMath::Pi()-true_phot_theta)*1000"

    gE1 = make_sigma_2(gdir+inE1[0], plot, tbin, tmin, tmax, inE1[1])
    #gE1x = make_sigma_2(gdir+inE1[0], plot, tbin, tmin, tmax, inE1[1])
    gE2 = make_sigma_2(gdir+inE2[0], plot, tbin, tmin, tmax, inE2[1])
    gE3 = make_sigma_2(gdir+inE3[0], plot, tbin, tmin, tmax, inE3[1])
    gE4 = make_sigma_2(gdir+inE4[0], plot, tbin, tmin, tmax, inE4[1])
    gE5 = make_sigma_2(gdir+inE5[0], plot, tbin, tmin, tmax, inE5[1])

    can = ut.box_canvas()
    frame = gPad.DrawFrame(tmin, smin, tmax, smax)
    frame.Draw()

    xtit = "#theta_{#gamma} (mrad)"
    ytit = "#frac{d#it{#sigma}}{d#theta_{#gamma}} (mb/mrad)"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.01, 0.01)

    gE1.SetLineColor(rt.kRed)
    #gE1x.SetLineColor(rt.kBlue)
    gE2.SetLineColor(rt.kYellow+1)
    gE3.SetLineColor(rt.kBlue)
    gE4.SetLineColor(rt.kGreen+1)
    gE5.SetLineColor(rt.kMagenta)

    gE1.Draw("lsame")
    #gE1x.Draw("lsame")
    gE2.Draw("lsame")
    gE3.Draw("lsame")
    gE4.Draw("lsame")
    gE5.Draw("lsame")

    leg = ut.prepare_leg(0.6, 0.66, 0.24, 0.25, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(gE4, "#it{e}-Au, 18 #times 110 GeV", "l")
    leg.AddEntry(gE5, "#it{e}-Au, 5 #times 41 GeV", "l")
    leg.AddEntry(gE1, "#it{ep}, 18 #times 275 GeV", "l")
    leg.AddEntry(gE2, "#it{ep}, 10 #times 100 GeV", "l")
    leg.AddEntry(gE3, "#it{ep}, 5 #times 41 GeV", "l")
    leg.Draw("same")

    dleg = ut.prepare_leg(0.55, 0.9, 0.24, 0.08, 0.035) # x, y, dx, dy, tsiz
    dleg.AddEntry(None, "Divergence included", "")
    #dleg.AddEntry(None, "No divergence", "")
    dleg.Draw("same")

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#make_theta_allE

#_____________________________________________________________________________
def make_sig_E():

    #cross section vs. photon energy

    ebin = 0.1
    emin = 0.5
    emax = 19

    smin = 0.9
    smax = 1e6

    gdir = "/home/jaroslav/sim/GETaLM_data/lumi/"

    inE1 = ["lumi_18x275_Lif_emin0p5_d200_beff3_5Mevt.root", 171.29]  #    129.63
    inE2 = ["lumi_10x100_Lif_emin0p5_beff3_5Mevt.root", 123.83]
    inE3 = ["lumi_5x41_Lif_emin0p5_beff3_5Mevt.root", 79.18]
    inE4 = ["lumi_eAu_18x110_Lif_emin0p5_d200_beff2_5Mevt.root", 963626.6]
    inE5 = ["lumi_eAu_5x41_Lif_emin0p5_beff2_5Mevt.root", 462904.4]

    plot = "true_phot_E"

    gE1 = make_sigma(gdir+inE1[0], plot, ebin, emin, emax, inE1[1])
    gE2 = make_sigma(gdir+inE2[0], plot, ebin, emin, emax, inE2[1])
    gE3 = make_sigma(gdir+inE3[0], plot, ebin, emin, emax, inE3[1])
    gE4 = make_sigma(gdir+inE4[0], plot, ebin, emin, emax, inE4[1])
    gE5 = make_sigma(gdir+inE5[0], plot, ebin, emin, emax, inE5[1])

    gStyle.SetPadTickY(1)
    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, smin, emax, smax)
    frame.Draw()

    ytit = "d#sigma / d#it{E}_{#gamma} (mb/GeV)"
    xtit = "#it{E}_{#gamma} (GeV)"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.4)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.01)

    #frame.GetYaxis().SetMoreLogLabels()

    gE1.SetLineColor(rt.kRed)
    gE2.SetLineColor(rt.kYellow+1)
    gE3.SetLineColor(rt.kBlue)
    gE4.SetLineColor(rt.kGreen+1)
    gE5.SetLineColor(rt.kMagenta)

    gE1.Draw("lsame")
    gE2.Draw("lsame")
    gE3.Draw("lsame")
    gE4.Draw("lsame")
    gE5.Draw("lsame")

    #test with cross section parametrization
    #sig_param = make_sigma_E_param()
    #sig_param.Draw("same")

    leg = ut.prepare_leg(0.6, 0.35, 0.24, 0.25, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(gE4, "#it{e}-Au, 18 #times 110 GeV", "l")
    leg.AddEntry(gE5, "#it{e}-Au, 5 #times 41 GeV", "l")
    leg.AddEntry(gE1, "#it{ep}, 18 #times 275 GeV", "l")
    leg.AddEntry(gE2, "#it{ep}, 10 #times 100 GeV", "l")
    leg.AddEntry(gE3, "#it{ep}, 5 #times 41 GeV", "l")
    leg.Draw("same")

    gPad.SetLogy()

    gPad.SetGrid()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#make_sig_E

#_____________________________________________________________________________
def make_E_theta():

    #energy and angle

    tmin = 0
    tmax = 2 # 5
    tbin = 0.03

    ebin = 0.3
    emin = 0.5
    emax = 18.5

    gdir = "/home/jaroslav/sim/GETaLM_data/lumi/"

    inp = "lumi_18x275_Lif_emin0p5_d200_beff3_5Mevt.root"

    infile = TFile.Open(gdir+inp)
    tree = infile.Get("ltree")

    can = ut.box_canvas()

    hEnT = ut.prepare_TH2D("hEnT", ebin, emin, emax, tbin, tmin, tmax)

    plot = "((TMath::Pi()-true_phot_theta)*1000)" + ":" + "(true_phot_E)"

    tree.Draw(plot+" >> hEnT")

    hEnT.SetXTitle("#it{E}_{#gamma} (GeV)")
    hEnT.SetYTitle("#theta_{#gamma} (mrad)")

    hEnT.SetTitleOffset(1.6, "Y")
    hEnT.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.13)

    hEnT.SetMinimum(0.98)
    hEnT.SetContour(300)

    leg = ut.prepare_leg(0.43, 0.84, 0.24, 0.12, 0.05) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "No divergence", "")
    leg.AddEntry(None, "#it{ep}, 18 #times 275 GeV", "")
    leg.SetTextColor(rt.kRed)
    leg.Draw("same")

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#make_E_theta

#_____________________________________________________________________________
def make_sigma(inp, plot, xbin, xmin ,xmax, sigma):

    #cross section plot from the tree

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)

    tree.Draw(plot+" >> hx")

    ut.norm_to_integral(hx, sigma)

    #gx = ut.h1_to_graph(hx)
    gx = ut.h1_to_graph_nz(hx)
    gx.SetLineWidth(3)

    return gx

#make_sigma

#_____________________________________________________________________________
def make_sigma_2(inp, plot, xbin, xmin ,xmax, sigma):

    #cross section in two binning intervals from the tree

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    #point to start longer bins
    xmid = 1
    bin2 = xbin*10.  #  4.

    hx = ut.prepare_TH1D_vec("hx", ut.get_bins_vec_2pt(xbin, bin2, xmin, xmax, xmid))

    tree.Draw(plot+" >> hx")

    #normalize to the width of each bin, necessary for variable binning
    for ibin in xrange(hx.GetNbinsX()+1):
        hx.SetBinContent(ibin, hx.GetBinContent(ibin)/hx.GetBinWidth(ibin))

    ut.norm_to_integral(hx, sigma)

    gx = ut.h1_to_graph(hx)
    gx.SetLineWidth(3)

    return gx

#make_sigma_2

#_____________________________________________________________________________
def make_sigma_E_param():

    #parametrization to dSigma/dE for test

    import ConfigParser

    sys.path.append('/home/jaroslav/sim/GETaLM/models')
    sys.path.append('/home/jaroslav/sim/GETaLM/base')

    from gen_zeus import gen_zeus

    parse = ConfigParser.RawConfigParser()
    parse.add_section("main")
    parse.set("main", "emin", "1") # GeV

    parse.set("main", "Ee", "18")
    parse.set("main", "Ep", "275")
    sig = gen_zeus(parse).dSigDe

    ut.set_F1(sig, rt.kBlue)

    return sig

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")



















