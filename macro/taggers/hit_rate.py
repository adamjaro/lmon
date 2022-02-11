#!/usr/bin/python3

import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
sys.path.append("../spectrometer")
import plot_utils as ut
from ParticleCounterSpect import ParticleCounterSpect

#_____________________________________________________________________________
def main():

    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm2ax2/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    #det = "s1"
    det = "s2"

    #mm
    xybin = 1.
    xymax = 110.

    infile = TFile.Open(inp)
    #number of interactions from event tree
    ni = infile.Get("event").GetEntries()
    #hits tree
    tree = infile.Get(det)

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xymax, xymax, xybin, -xymax, xymax)
    tree.Draw("y:x >> hXY")

    #scale to hits per unit area per second
    counter_hits = ParticleCounterSpect()

    # 18x275 GeV
    #counter_hits.sigma_tot = 0.05326 # mb, quasi-real
    #counter_hits.sigma_tot = 0.0547 # mb, Pythia6
    counter_hits.sigma_tot = 171.29 # mb, bremsstrahlung
    counter_hits.lumi_cmsec = 1.54e33 # cm^-2 sec^-1
    counter_hits.nbunch = 290
    counter_hits.Ee = 18. # GeV

    scale = counter_hits.get_scale()
    print("scale:", scale)
    lam = scale["lambda"]
    tb = scale["Tb"]

    #bin area in mm^2
    bin_area = xybin**2

    nhits_all = 0.

    min_rate = 9e9
    for ix in range(1, hXY.GetNbinsX()+1):
        for iy in range(1, hXY.GetNbinsY()+1):

            nh = hXY.GetBinContent(ix, iy)
            nhits_all += nh

            #hits in bunch crossing
            nhb = (nh/ni)*lam

            #rate per area, mm^-2 sec^-1
            rA = (1.-np.e**(-nhb))*(1./tb)*(1./bin_area)
            #print(rA)

            if rA < min_rate and nh > 0:
                min_rate = rA

            hXY.SetBinContent(ix, iy, rA)

    #hits per interaction
    print("Hits per interaction:", nhits_all/ni)

    #integrated rate
    rate_all = (1.-np.e**(-(nhits_all/ni)*lam))*(1./tb)
    print("Integrated rate (MHz):", 1e-6*rate_all)

    #print("min_rate:", min_rate)

    hXY.SetMinimum(min_rate)
    hXY.SetContour(300)

    ytit = "#it{y} (mm)"
    xtit = "#it{x} (mm)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    hXY.SetZTitle("Event rate #it{R_{A}} (mm^{-2} s^{-1})")
    hXY.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.15)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()



