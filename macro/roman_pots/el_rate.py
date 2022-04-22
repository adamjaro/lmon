#!/usr/bin/python3

import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TDatabasePDG

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = const_L
    func[1] = bfreq

    func[iplot]()

#main

#_____________________________________________________________________________
def const_L():

    #assumption of constant instantaneous luminosity, producing an approximation
    #of a continuous beam of interacting particles

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5a/hits_tag.root"

    #sigma_tot = 0.05326 # mb, quasi-real
    sigma_tot = 274.7779 # mb, lumi_18x275_bx_emin0p1_T3p3_10Mevt.root
    lumi_cmsec = 1.54e33 # cm^-2 sec^-1
    #Nsim = 5e6 # number of simulated events
    Nsim = 1e7 # number of simulated events

    #mm
    xybin = 1
    xymax = 80

    #det = "s1A"
    det = "s2A"

    #production rate
    Rprod = sigma_tot*lumi_cmsec*1e-27
    print("Rprod:", Rprod)

    # fR = Rprod/(Nsim*A) ,  A = bin area
    fR = Rprod/(Nsim*xybin*xybin)

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()
    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)
    tree.Draw("y:x >> hxy")

    min_rate = 9e9
    sum_rate = 0.
    for ix in range(1, hxy.GetNbinsX()+1):
        for iy in range(1, hxy.GetNbinsY()+1):

            nh = hxy.GetBinContent(ix, iy)

            #rate per area
            rA = nh*fR

            sum_rate += rA*xybin*xybin

            if rA < min_rate and nh > 0:
                min_rate = rA

            hxy.SetBinContent(ix, iy, rA)

    print("Sum rate (Hz):", sum_rate)

    ytit = "#it{y} (mm)"
    xtit = "#it{x} (mm)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.4, 1.4)

    #hxy.SetZTitle("Counts")
    hxy.SetZTitle("Event rate #it{R_{A}} (mm^{-2} s^{-1})")
    hxy.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.15)

    hxy.SetMinimum(min_rate)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#const_L

#_____________________________________________________________________________
def bfreq():

    #fixed bunch crossing frequency

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5a/hits_tag.root"

    #sigma_tot = 0.05326 # mb, quasi-real
    sigma_tot = 274.7779 # mb, lumi_18x275_bx_emin0p1_T3p3_10Mevt.root
    lumi_cmsec = 1.54e33 # cm^-2 sec^-1
    nbunch = 290 # number of bunches
    Ee = 18. # GeV, electron beam energy
    #Nsim = 5e6 # number of simulated events
    Nsim = 1e7 # number of simulated events

    #mm
    xybin = 1
    xymax = 80

    #det = "s1A"
    det = "s2A"

    #production rate
    #Rprod = sigma_tot*lumi_cmsec*1e-27
    #print("Rprod:", Rprod)

    # fR = Rprod/(Nsim*A) ,  A = bin area
    #fR = Rprod/(Nsim*xybin*xybin)

    #collider circumference, speed of light, electron mass
    circ = 3834. # m
    cspeed = 299792458. # m sec^-1
    me = TDatabasePDG.Instance().GetParticle(11).Mass() # GeV

    #beam velocity (units of c)
    beta = np.sqrt(Ee**2-me**2)/Ee
    print("Beta:", beta)
    print("Orbit period (micro sec):", 1e6*circ/(beta*cspeed))

    #bunch spacing, sec
    Tb = circ/(beta*cspeed*nbunch)
    print("Bunch spacing (micro sec):", 1e6*Tb)
    print("Bunch frequency (MHz):", 1e-6/Tb)

    #luminosity per bunch crossing, mb^-1
    Lb = lumi_cmsec*1e-27*Tb
    print("Luminosity per bunch crossing, mb^-1:", Lb)
    print("Mean number of interactions per bunch crossing:", sigma_tot*Lb)
    print("Probability for at least one interaction in bunch crossing:", (1.-np.e**(-sigma_tot*Lb)))

    lam = sigma_tot*Lb

    #open the input
    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()
    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)
    tree.Draw("y:x >> hxy")

    min_rate = 9e9
    sum_rate = 0.
    for ix in range(1, hxy.GetNbinsX()+1):
        for iy in range(1, hxy.GetNbinsY()+1):

            nh = hxy.GetBinContent(ix, iy)

            #hits in bunch crossing
            nhb = (nh/Nsim)*lam

            #rate per area
            rA = (1.-np.e**(-nhb))*(1./Tb)*(1./(xybin*xybin))

            sum_rate += rA*xybin*xybin

            if rA < min_rate and nh > 0:
                min_rate = rA

            hxy.SetBinContent(ix, iy, rA)

    print("Sum rate (Hz):", sum_rate)

    ytit = "#it{y} (mm)"
    xtit = "#it{x} (mm)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.4, 1.4)

    #hxy.SetZTitle("Counts")
    hxy.SetZTitle("Event rate #it{R_{A}} (mm^{-2} s^{-1})")
    hxy.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.15)

    hxy.SetMinimum(min_rate)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#bfreq

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

























