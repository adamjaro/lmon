#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = rate_lQ2

    func[iplot]()

#main

#_____________________________________________________________________________
def rate_lQ2():

    #production rate as a function of log_10(Q^2) for signal and background

    #log_10(GeV^2)
    qbin1 = 0.1
    qbin2 = 0.2
    qmin = -10
    qmax = -0.2

    #MHz
    rmin = 1e-6
    rmax = 1e2

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v1.root"

    #number of simulated events
    nsim = 5000*1999

    #det = "s1_tracks"
    det = "s2_tracks"

    #18x275 GeV
    sigma_qr = 0.053266 # mb, quasi-real cross section, qr_bx_18x275_T3p3_10Mevt.log
    lumi_cmsec = 1.54e33 # cm^-2 sec^-1, instantaneous luminosity, 
    rate_bkg = 22.6760075 # MHz, bunch frequency, qr_bx_18x275_T3p3_10Mevt.log

    #quasi-real production rate
    rate_qr = sigma_qr*lumi_cmsec*1e-27 # Hz

    print("Quasi-real production rate (Hz):", rate_qr)

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    #background
    hbkg = ut.prepare_TH1D("hbkg", qbin2, qmin, qmax)
    tree.Draw("TMath::Log10(rec_Q2) >> hbkg", "itrk!=1")
    ut.norm_to_integral(hbkg, rate_bkg)

    #quasi-real signal
    hqr = ut.prepare_TH1D("hqr", qbin1, qmin, qmax)
    tree.Draw("TMath::Log10(rec_Q2) >> hqr", "itrk==1")
    ut.norm_to_integral(hqr, (hqr.GetEntries()/nsim)*rate_qr*1e-6) # rate in MHz

    can = ut.box_canvas()
    frame = gPad.DrawFrame(qmin, rmin, qmax, rmax)
    frame.Draw()

    hbkg.Draw("e1same")

    hqr.SetLineColor(rt.kRed)
    hqr.Draw("e1same")

    gPad.SetLogy()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")





#rate_lQ2

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()





















