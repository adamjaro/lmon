#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0
    funclist = []
    funclist.append( make_theta_allE ) # 0

    funclist[iplot]()

#main

#_____________________________________________________________________________
def make_theta_allE():

    #theta for all beam energies

    tmin = 0
    tmax = 5
    tbin = 0.05
    smax = 1e4
    smin = 1e-2

    gdir = "/home/jaroslav/sim/GETaLM_data/lumi/"

    #inE1 = ["lumi_18x275_Lif_emin0p1_1Mevt.root", 276.35]
    #inE2 = ["lumi_10x100_Lif_emin0p1_1Mevt.root", 217.09]
    #inE3 = ["lumi_5x41_Lif_emin0p1_1Mevt.root", 159.33]

    inE1 = ["lumi_18x275_Lif_emin0p5_beff2_5Mevt.root", 171.29]
    inE2 = ["lumi_10x100_Lif_emin0p5_beff2_5Mevt.root", 123.83]
    inE3 = ["lumi_5x41_Lif_emin0p5_beff2_5Mevt.root", 79.18]

    plot = "(TMath::Pi()-phot_theta)*1000"
    #plot = "(TMath::Pi()-true_phot_theta)*1000"

    gE1 = make_sigma(gdir+inE1[0], plot, tbin, tmin, tmax, inE1[1])
    gE2 = make_sigma(gdir+inE2[0], plot, tbin, tmin, tmax, inE2[1])
    gE3 = make_sigma(gdir+inE3[0], plot, tbin, tmin, tmax, inE3[1])

    can = ut.box_canvas()
    frame = gPad.DrawFrame(tmin, smin, tmax, smax)
    frame.Draw()

    xtit = "#theta_{#gamma} (mrad)"
    ytit = "#frac{d#it{#sigma}}{d#theta_{#gamma}} (mb/mrad)"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.01, 0.01)

    gE1.SetLineColor(rt.kRed)
    gE2.SetLineColor(rt.kYellow+1)
    gE3.SetLineColor(rt.kBlue)

    gE1.Draw("lsame")
    gE2.Draw("lsame")
    gE3.Draw("lsame")

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#make_theta_allE

#_____________________________________________________________________________
def make_sigma(inp, plot, xbin, xmin ,xmax, sigma):

    infile = TFile.Open(inp)
    tree = infile.Get("ltree")

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)

    tree.Draw(plot+" >> hx")

    ut.norm_to_integral(hx, sigma)

    gx = ut.h1_to_graph(hx)
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


