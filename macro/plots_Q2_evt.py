#!/usr/bin/env python

#/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath

import plot_utils as ut

#_____________________________________________________________________________
def main():

    infile = "../data/test/lmon.root"
    #infile = "../data/lmon_18x275_qr_lowQ2_47p2cm_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xB_yA_lowQ2_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xB_yA_lowQ2_B2eRv2_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xB_yB_lowQ2_1Mevt.root"

    iplot = 0
    funclist = []
    funclist.append( evt_Log10_Q2 ) # 0
    funclist.append( el_phi_tag ) # 1
    funclist.append( el_theta_tag ) # 2
    funclist.append( el_theta_phi_tag ) # 3
    funclist.append( evt_Log10_Q2_y ) # 4
    funclist.append( evt_Q2_theta ) # 5

    #kinematics formula for log_10(Q2)
    global gL10Q2
    gL10Q2 = "TMath::Log10(2.*18.*el_gen*(1.-TMath::Cos(TMath::Pi()-el_theta)))"

    #selection for hit in tagger, contains B2eR aperture
    global gQ2sel
    gQ2sel = "lowQ2_IsHit==1 && TMath::Pi()-el_theta<0.01021"

    #open the input and run
    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("DetectorTree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def evt_Log10_Q2():

    #plot the log_10(Q^2) using the kinematics formula

    lqbin = 5e-2
    #lqmin = -6
    lqmin = -10
    lqmax = 2
    #lqbin = 5e-3
    #lqmin = -2.2
    #lqmax = -1.8

    hLog10Q2 = ut.prepare_TH1D("hLog10Q2", lqbin, lqmin, lqmax)
    hLog10Q2Tag = ut.prepare_TH1D("hLog10Q2Tag", lqbin, lqmin, lqmax)

    tree.Draw(gL10Q2+" >> hLog10Q2")
    tree.Draw(gL10Q2+" >> hLog10Q2Tag", gQ2sel)

    print "All events:", hLog10Q2.GetEntries()
    print "Selected  :", hLog10Q2Tag.GetEntries()

    can = ut.box_canvas()

    ut.put_yx_tit(hLog10Q2, "Events", "log_{10}(#it{Q}^{2})", 1.4, 1.2)

    hLog10Q2.Draw()
    hLog10Q2Tag.Draw("e1same")

    #hLog10Q2Tag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Log10_Q2

#_____________________________________________________________________________
def el_phi_tag():

    #electron generated azimuthal angle for electrons hitting the tagger

    #bins in phi
    pbin = 1e-1
    pmin = -TMath.Pi()
    pmax = TMath.Pi()

    #interval in log_10(Q^2)
    lqmin = -1.5
    lqmax = -0.9
    lqsel = gL10Q2+" > "+str(lqmin)+" && "+gL10Q2+" < "+str(lqmax)

    #bins for selected log_10(Q^2)
    pbins = 2e-2

    can = ut.box_canvas()

    hPhiTag = ut.prepare_TH1D("hPhiTag", pbin, pmin, pmax)
    hPhiTagQ2sel = ut.prepare_TH1D("hPhiTagQ2sel", pbins, pmin, pmax)

    tree.Draw("el_phi >> hPhiTag", "lowQ2_IsHit == 1")
    tree.Draw("el_phi >> hPhiTagQ2sel", "lowQ2_IsHit==1"+" && "+lqsel)

    gPad.SetLogy()

    hPhiTag.Draw()
    hPhiTagQ2sel.Draw("e1same")
    #hPhiTagQ2sel.Draw()

    hPhiTag.SetMinimum(0.3)

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_phi_tag

#_____________________________________________________________________________
def el_theta_tag():

    #electron generated polar angle for electrons hitting the tagger

    #bins in theta
    tbin = 5e-4
    tmin = 0
    tmax = 2.5e-2

    #interval in log_10(Q^2)
    lqmin = -1.5
    lqmax = -0.9
    lqsel = gL10Q2+" > "+str(lqmin)+" && "+gL10Q2+" < "+str(lqmax)

    #bins for selected log_10(Q^2)
    #pbins = 2e-2

    can = ut.box_canvas()

    hThetaTag = ut.prepare_TH1D("hThetaTag", tbin, tmin, tmax)
    hThetaTagQ2sel = ut.prepare_TH1D("hThetaTagQ2sel", tbin, tmin, tmax)

    tree.Draw("TMath::Pi()-el_theta >> hThetaTag", gQ2sel)
    #tree.Draw("TMath::Pi()-el_theta >> hThetaTagQ2sel", "lowQ2_IsHit==1"+" && "+lqsel)

    gPad.SetLogy()

    hThetaTag.Draw()
    #hThetaTagQ2sel.Draw("e1same")

    #hThetaTag.SetMinimum(0.3)

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_theta_tag

#_____________________________________________________________________________
def el_theta_phi_tag():

    #electron generated polar and azimuthal angle for electrons hitting the tagger

    #bins in theta
    tbin = 5e-4
    tmin = 0
    tmax = 2.5e-2

    #bins in phi
    pbin = 1e-1
    pmin = -TMath.Pi()
    pmax = TMath.Pi()

    can = ut.box_canvas()

    hThetaPhi = ut.prepare_TH2D("hThetaPhi", tbin, tmin, tmax, pbin, pmin, pmax)
    hThetaPhiTag = ut.prepare_TH2D("hThetaPhiTag", tbin, tmin, tmax, pbin, pmin, pmax)

    tree.Draw("el_phi:TMath::Pi()-el_theta >> hThetaPhi")
    tree.Draw("el_phi:TMath::Pi()-el_theta >> hThetaPhiTag", gQ2sel)

    gPad.SetLogx()
    #gPad.SetLogz()

    #hThetaPhi.Draw()
    hThetaPhiTag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_theta_phi_tag

#_____________________________________________________________________________
def evt_Log10_Q2_y():

    #log_10(Q^2) and y

    lqbin = 5e-2
    lqmin = -5
    lqmax = -1.5

    ybin = 1e-2
    ymin = 0.06
    ymax = 0.8

    yform = "(18.-el_gen)/18."

    hLog10Q2yTag = ut.prepare_TH2D("hLog10Q2yTag", ybin, ymin, ymax, lqbin, lqmin, lqmax)

    tree.Draw(gL10Q2+":"+yform+" >> hLog10Q2yTag", gQ2sel)

    can = ut.box_canvas()

    hLog10Q2yTag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Log10_Q2_y

#_____________________________________________________________________________
def evt_Q2_theta():

    #Q^2 and theta

    qbin = 5e-6
    qmin = 1e-5
    qmax = 9e-1

    tbin = 1e-4
    tmin = 0
    tmax = 0.011

    qform = "2.*18.*el_gen*(1.-TMath::Cos(TMath::Pi()-el_theta))"

    hQ2thetaTag = ut.prepare_TH2D("hQ2thetaTag", tbin, tmin, tmax, qbin, qmin, qmax)

    tree.Draw(qform+":TMath::Pi()-el_theta >> hQ2thetaTag", gQ2sel)

    can = ut.box_canvas()

    gPad.SetLogy()
    gPad.SetLogz()

    hQ2thetaTag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Q2_theta

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()












