#!/usr/bin/env python

#/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "../data/test/lmon.root"
    #infile = "../data/lmon_18x275_qr_lowQ2_47p2cm_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xB_yA_lowQ2_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xB_yA_lowQ2_B2eRv2_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xD_yC_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qa_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qb_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qb_beff2_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qd_beff2_5Mevt.root"
    infile = "../data/lmon_py_18x275_Q2all_beff2_5Mevt.root"
    #infile = "../data/ir6/lmon_pythia_5M_beff2_5Mevt_v2.root"
    #infile = "../data/ir6/lmon_pythia_5M_beff2_1p5T_5Mevt_v2.root"
    #infile = "../data/ir6_close/lmon_pythia_5M_beff2_close_5Mevt.root"
    #infile = "/home/jaroslav/sim/lgen/data/lgen_18x275_qr_Qd_beff2_5Mevt.root"

    iplot = 16
    funclist = []
    funclist.append( evt_Log10_Q2 ) # 0
    funclist.append( el_phi_tag ) # 1
    funclist.append( el_theta_tag ) # 2
    funclist.append( el_theta_phi_tag ) # 3
    funclist.append( evt_Log10_Q2_y ) # 4
    funclist.append( evt_Q2_theta ) # 5
    funclist.append( evt_lx_ly ) # 6
    funclist.append( evt_log10_Q2_theta ) # 7
    funclist.append( el_en_tag ) # 8
    funclist.append( el_log10_theta_tag ) # 9
    funclist.append( el_en_log10_theta_tag ) # 10
    funclist.append( evt_Log10_Q2_x ) # 11
    funclist.append( evt_Log10_Q2_separate ) # 12
    funclist.append( evt_Log10_Q2_ecal_compare ) # 13
    funclist.append( el_en_theta_tag ) # 14
    funclist.append( evt_true_lQ2_lx ) # 15
    funclist.append( evt_true_lx_ly ) # 16
    funclist.append( evt_true_lx_ly_lQ2 ) # 17
    funclist.append( rel_true_Q2_el_Q2 ) # 18
    funclist.append( evt_true_lQ2_lx_separate ) # 19
    funclist.append( evt_true_lx ) # 20
    funclist.append( evt_Q2_el_Q2 ) # 21
    funclist.append( evt_true_lQ2_ly_separate ) # 22

    #kinematics formula for log_10(Q2)
    global gL10Q2
    gL10Q2 = "TMath::Log10(2.*18.*el_gen*(1.-TMath::Cos(TMath::Pi()-el_theta)))"

    #selection for hit in tagger, contains B2eR aperture
    global gQ2sel
    #gQ2sel = "lowQ2_IsHit==1 && TMath::Pi()-el_theta<0.01021"
    #gQ2sel = "lowQ2_IsHit==1"
    #gQ2sel = "lowQ2s1_IsHit==1"
    gQ2sel = "lowQ2s2_IsHit==1"
    #gQ2sel = "ecal_IsHit==1"
    #gQ2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1"
    #gQ2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"

    #open the input and run
    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("DetectorTree")
    #tree = inp.Get("ltree")
    #tree.Print()

    funclist[iplot]()

#main

#_____________________________________________________________________________
def evt_Log10_Q2():

    #plot the log_10(Q^2) using the kinematics formula

    lqbin = 5e-2
    #lqmin = -6
    lqmin = -11
    lqmax = 5
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

    ytit = "Events / {0:.3f}".format(lqbin)
    ut.put_yx_tit(hLog10Q2, ytit, "log_{10}(#it{Q}^{2})", 1.4, 1.2)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.03, 0.02)

    ut.line_h1(hLog10Q2, rt.kBlue, 3)
    ut.line_h1(hLog10Q2Tag, rt.kRed, 3)

    gPad.SetLogy()
    gPad.SetGrid()

    hLog10Q2.Draw()
    hLog10Q2Tag.Draw("e1same")

    hLog10Q2.SetMaximum(2e5) # for qr

    leg = ut.prepare_leg(0.2, 0.83, 0.2, 0.1, 0.035)
    leg.AddEntry(hLog10Q2, "All electrons from quasi-real photoproduction", "l")
    #leg.AddEntry(hLog10Q2, "All Pythia6 scattered electrons", "l")
    leg.AddEntry(hLog10Q2Tag, "Electrons hitting the tagger", "l")
    leg.Draw("same")

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
    tbin = 1e-4
    tmin = 3e-4
    tmax = 1.1e-2

    #bins in phi
    pbin = 1e-1
    pmin = -TMath.Pi()
    pmax = TMath.Pi()

    can = ut.box_canvas()

    hThetaPhi = ut.prepare_TH2D("hThetaPhi", tbin, tmin, tmax, pbin, pmin, pmax)
    hThetaPhiTag = ut.prepare_TH2D("hThetaPhiTag", tbin, tmin, tmax, pbin, pmin, pmax)

    tree.Draw("el_phi:TMath::Pi()-el_theta >> hThetaPhi")
    tree.Draw("el_phi:TMath::Pi()-el_theta >> hThetaPhiTag", gQ2sel)

    ytit = "Azimuthal angle #varphi (rad) / {0:.3f}".format(pbin)
    xtit = "Polar angle #theta (rad) / {0:.2f} mrad".format(tbin*1e3)
    ut.put_yx_tit(hThetaPhiTag, ytit, xtit, 1.2, 1.4)

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.03, 0.12)

    gPad.SetLogx()
    #gPad.SetLogz()

    hThetaPhiTag.GetXaxis().SetMoreLogLabels()

    #hThetaPhi.Draw()
    hThetaPhiTag.Draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_theta_phi_tag

#_____________________________________________________________________________
def evt_Log10_Q2_y():

    #log_10(Q^2) and y

    lqbin = 5e-2
    #lqmin = -5
    lqmin = -10
    lqmax = -1.5

    ybin = 1e-2
    #ymin = 0.06
    ymin = 0
    ymax = 0.8

    yform = "(18.-el_gen)/18."

    hLog10Q2yTag = ut.prepare_TH2D("hLog10Q2yTag", ybin, ymin, ymax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw(gL10Q2+":"+yform+" >> hLog10Q2yTag", gQ2sel)

    ut.put_yx_tit(hLog10Q2yTag, "log_{10}(#it{Q}^{2})", "y", 1.6, 1.4)

    gPad.SetLogx()

    hLog10Q2yTag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Log10_Q2_y

#_____________________________________________________________________________
def evt_Q2_theta():

    #Q^2 and theta

    qbin = 5e-6
    qmin = 1e-10
    qmax = 1e-1

    tbin = 1e-4
    tmin = 0
    tmax = 0.011

    qform = "2.*18.*el_gen*(1.-TMath::Cos(TMath::Pi()-el_theta))"

    hQ2thetaTag = ut.prepare_TH2D("hQ2thetaTag", tbin, tmin, tmax, qbin, qmin, qmax)

    tree.Draw(qform+":TMath::Pi()-el_theta >> hQ2thetaTag", gQ2sel)

    ytit = "Q^{2} / 5x10^{-6} GeV^{2}"
    xtit = "Polar angle #theta (rad) / {0:.2f} mrad".format(tbin*1e3)
    ut.put_yx_tit(hQ2thetaTag, ytit, xtit, 1.6, 1.4)

    can = ut.box_canvas()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.11)

    gPad.SetLogy()
    gPad.SetLogz()

    hQ2thetaTag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Q2_theta

#_____________________________________________________________________________
def evt_lx_ly():

    #log_10(x) and log_10(y)

    xbin = 0.01
    #xbin = 0.1
    xmin = -14
    xmax = 0

    ybin = 0.01
    #ybin = 0.1
    ymin = -5
    ymax = 0

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)
    hXYtag = ut.prepare_TH2D("hXYtag", xbin, xmin, xmax, ybin, ymin, ymax)

    can = ut.box_canvas()

    #yform = "(18.-el_gen)/18."
    yform = "1.-(1.-TMath::Cos(el_theta))*el_gen/(2.*18.)"
    #yform = 
    Q2form = "2.*18.*el_gen*(1.-TMath::Cos(TMath::Pi()-el_theta))"
    xform = Q2form+"/(("+yform+")*19800.82)"

    lyform = "TMath::Log10("+yform+")"
    lxform = "TMath::Log10("+xform+")"

    tree.Draw(lyform+":"+lxform+" >> hXY")
    tree.Draw(lyform+":"+lxform+" >> hXYtag", gQ2sel)

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)
    ut.put_yx_tit(hXYtag, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()
    #hXYtag.Draw()

    gPad.SetGrid()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_lx_ly

#_____________________________________________________________________________
def evt_log10_Q2_theta():

    #log_10(Q^2) and theta

    lqbin = 0.01
    lqmin = -8
    lqmax = -1

    tbin = 1e-4
    tmin = 0
    tmax = 0.011

    hlQ2thetaTag = ut.prepare_TH2D("hlQ2thetaTag", tbin, tmin, tmax, lqbin, lqmin, lqmax)

    tree.Draw(gL10Q2+":TMath::Pi()-el_theta >> hlQ2thetaTag", gQ2sel)

    ytit = "log_{10}(Q^{2}) / "+"{0:.3f}".format(lqbin)
    xtit = "Polar angle #theta (rad) / {0:.2f} mrad".format(tbin*1e3)
    ut.put_yx_tit(hlQ2thetaTag, ytit, xtit, 1.6, 1.4)

    can = ut.box_canvas()

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.12)

    #gPad.SetLogx()
    gPad.SetLogz()

    hlQ2thetaTag.Draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_log10_Q2_theta

#_____________________________________________________________________________
def el_en_tag():

    #energy for electrons hitting the tagger

    #bins in energy
    ebin = 0.1
    emin = 8.5
    emax = 18

    can = ut.box_canvas()

    #hEnTag = ut.prepare_TH1D("hEnTag", ebin, emin, emax)
    hEnTag = ut.prepare_TH1D_n("hEnTag", 10, emin, emax)

    tree.Draw("el_gen >> hEnTag", gQ2sel)

    hEnTag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_en_tag

#_____________________________________________________________________________
def el_log10_theta_tag():

    #electron generated log_10 of polar angle for electrons hitting the tagger

    #bins in log_10(theta)
    ltbin = 0.1
    ltmin = -5.5
    ltmax = -1.5

    can = ut.box_canvas()

    #hThetaTag = ut.prepare_TH1D("hThetaTag", ltbin, ltmin, ltmax)
    hThetaTag = ut.prepare_TH1D_n("hThetaTag", 30, ltmin, ltmax)

    tree.Draw("TMath::Log10(TMath::Pi()-el_theta) >> hThetaTag", gQ2sel)

    #gPad.SetLogy()

    hThetaTag.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_log10_theta_tag

#_____________________________________________________________________________
def el_en_log10_theta_tag():

    #electron generated energy and log_10 of polar angle for electrons hitting the tagger

    #bins in log_10(theta)
    #ltbin = 0.1
    #ltmin = -7
    #ltmax = -1.2
    ltbin = 0.01
    ltmin = -2
    ltmax = 0

    #bins in energy
    #ebin = 0.1
    #emin = 2
    #emax = 20
    ebin = 0.1
    emin = 0
    emax = 20

    #sel = "lowQ2s1_IsHit==1"
    #sel = "lowQ2s2_IsHit==1"
    sel = "ecal_IsHit==1"
    #gQ2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"

    can = ut.box_canvas()

    hEnThetaTag = ut.prepare_TH2D("hEnThetaTag", ltbin, ltmin, ltmax, ebin, emin, emax)

    tree.Draw("el_gen:TMath::Log10(TMath::Pi()-el_theta) >> hEnThetaTag", sel)

    ytit = "#it{E}_{e} / "+"{0:.1f} GeV".format(ebin)
    xtit = "log_{10}(#theta_{e}) / "+"{0:.2f} rad".format(ltbin)
    ut.put_yx_tit(hEnThetaTag, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.11)

    gPad.SetLogz()

    gPad.SetGrid()

    hEnThetaTag.SetMinimum(0.98)
    hEnThetaTag.SetContour(300)

    #hEnThetaTag.SetContour(10)
    hEnThetaTag.Draw("colz")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_en_log10_theta_tag

#_____________________________________________________________________________
def evt_Log10_Q2_x():

    #log_10(Q^2) and x

    lqbin = 5e-2
    #lqmin = -5
    lqmin = -10
    lqmax = -1

    #xbin = 0.01
    xbin = 0.1
    xmin = -14
    xmax = -0.3

    yform = "1.-(1.-TMath::Cos(el_theta))*el_gen/(2.*18.)"
    Q2form = "2.*18.*el_gen*(1.-TMath::Cos(TMath::Pi()-el_theta))"
    xform = Q2form+"/(("+yform+")*19800.82)"

    lQ2form = "TMath::Log10("+Q2form+")"
    lxform = "TMath::Log10("+xform+")"

    hLog10Q2xTag = ut.prepare_TH2D("hLog10Q2xTag", xbin, xmin, xmax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw(lQ2form+":"+lxform+" >> hLog10Q2xTag", gQ2sel)
    #tree.Draw(lQ2form+":"+lxform+" >> hLog10Q2xTag")

    ytit = "log_{10}(#it{Q}^{2})"+" / {0:.3f}".format(lqbin)+" GeV^{2}"
    xtit = "log_{10}(#it{x})"+" / {0:.1f}".format(xbin)
    ut.put_yx_tit(hLog10Q2xTag, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.11)

    gPad.SetGrid()

    hLog10Q2xTag.Draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Log10_Q2_x

#_____________________________________________________________________________
def evt_Log10_Q2_separate():

    #log_10(Q^2) for each tagger station and ecal separately, kinematics formula or true Q^2

    lqbin = 5e-2
    #lqmin = -6
    lqmin = -11
    lqmax = 5
    #lqbin = 5e-3
    #lqmin = -2.2
    #lqmax = -1.8

    #gQ2sel = "lowQ2s1_IsHit==1"
    #gQ2sel = "lowQ2s2_IsHit==1"
    #gQ2sel = "ecal_IsHit==1"

    #override to generator true Q2
    #gL10Q2 = "TMath::Log10(true_Q2)"

    hLog10Q2 = ut.prepare_TH1D("hLog10Q2", lqbin, lqmin, lqmax)
    hQ2s1 = ut.prepare_TH1D("hQ2s1", lqbin, lqmin, lqmax)
    hQ2s2 = ut.prepare_TH1D("hQ2s2", lqbin, lqmin, lqmax)
    hQ2ecal = ut.prepare_TH1D("hQ2ecal", lqbin, lqmin, lqmax)
    #hLog10Q2Tag = ut.prepare_TH1D("hLog10Q2Tag", lqbin, lqmin, lqmax)

    tree.Draw(gL10Q2+" >> hLog10Q2")
    tree.Draw(gL10Q2+" >> hQ2s1", "lowQ2s1_IsHit==1")
    tree.Draw(gL10Q2+" >> hQ2s2", "lowQ2s2_IsHit==1")
    tree.Draw(gL10Q2+" >> hQ2ecal", "ecal_IsHit==1")

    print "All events:", hLog10Q2.GetEntries()
    #print "Selected  :", hLog10Q2Tag.GetEntries()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(lqmin, 1, lqmax, 1e6)
    frame.Draw()

    ytit = "Events / {0:.3f}".format(lqbin)
    #xtit = "log_{10}(#it{Q}^{2})"
    xtit = "log_{10}(#it{Q}^{2}_{e})"
    #ut.put_yx_tit(hLog10Q2, ytit, "log_{10}(#it{Q}^{2})", 1.4, 1.2)
    ut.put_yx_tit(frame, ytit, xtit, 1.4, 1.2)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.03, 0.02)

    ut.line_h1(hLog10Q2, rt.kBlack, 3)
    ut.line_h1(hQ2s1, rt.kYellow+1, 3)
    ut.line_h1(hQ2s2, rt.kGreen+1, 3)
    ut.line_h1(hQ2ecal, rt.kBlue, 3)

    gPad.SetLogy()
    gPad.SetGrid()

    hLog10Q2.Draw("e1same")
    hQ2s1.Draw("e1same")
    hQ2s2.Draw("e1same")
    hQ2ecal.Draw("e1same")

    #hLog10Q2.SetMaximum(2e5) # for qr

    leg = ut.prepare_leg(0.2, 0.78, 0.2, 0.16, 0.035)
    leg.AddEntry(hLog10Q2, "All quasi-real electrons", "l")
    #leg.AddEntry(hLog10Q2, "All Pythia6 events", "l")
    leg.AddEntry(hQ2s1, "Tagger 1", "l")
    leg.AddEntry(hQ2s2, "Tagger 2", "l")
    leg.AddEntry(hQ2ecal, "ECAL", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Log10_Q2_separate

#_____________________________________________________________________________
def evt_Log10_Q2_ecal_compare():

    #compare log_10(Q^2) from ecal for two separate inputs

    infile1 = "../data/ir6/lmon_pythia_5M_beff2_5Mevt_v2.root"
    #infile2 = "../data/ir6_close/lmon_pythia_5M_beff2_close_5Mevt.root"
    #infile2 = "../data/ir6/lmon_pythia_5M_beff2_1p5T_5Mevt.root"
    infile2 = "../data/ir6/lmon_pythia_5M_beff2_1p5T_5Mevt_v2.root"

    lqbin = 5e-2
    lqmin = -2.5
    lqmax = 2.5

    inp1 = TFile.Open(infile1)
    inp2 = TFile.Open(infile2)
    tree1 = inp1.Get("DetectorTree")
    tree2 = inp2.Get("DetectorTree")

    hQ2ecal = ut.prepare_TH1D("hQ2ecal", lqbin, lqmin, lqmax)
    hQ2ecal_close = ut.prepare_TH1D("hQ2ecal_close", lqbin, lqmin, lqmax)

    tree1.Draw(gL10Q2+" >> hQ2ecal", "ecal_IsHit==1")
    tree2.Draw(gL10Q2+" >> hQ2ecal_close", "ecal_IsHit==1")

    print "All events:", hQ2ecal.GetEntries()
    #print "Selected  :", hLog10Q2Tag.GetEntries()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(lqmin, 10, lqmax, 1e5)
    frame.Draw()

    ytit = "Events / {0:.3f}".format(lqbin)
    ut.put_yx_tit(frame, ytit, "log_{10}(#it{Q}^{2})", 1.4, 1.2)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.03, 0.02)

    ut.line_h1(hQ2ecal, rt.kBlue, 3)
    ut.line_h1(hQ2ecal_close, rt.kRed, 3)

    #hQ2ecal.SetMinimum(10)

    gPad.SetLogy()
    gPad.SetGrid()

    hQ2ecal.Draw("e1same")
    hQ2ecal_close.Draw("e1same")

    #hLog10Q2.SetMaximum(2e5) # for qr

    leg = ut.prepare_leg(0.6, 0.83, 0.2, 0.1, 0.035)
    #leg.AddEntry(hLog10Q2, "All electrons from quasi-real photoproduction", "l")
    #leg.AddEntry(hLog10Q2, "All Pythia6 scattered electrons", "l")
    #leg.AddEntry(hLog10Q2Tag, "Electrons hitting the tagger", "l")
    leg.AddEntry(hQ2ecal, "Default geometry", "l")
    #leg.AddEntry(hQ2ecal_close, "Magnets in central det", "l")
    leg.AddEntry(hQ2ecal_close, "1.5T solenoid", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Log10_Q2_ecal_compare

#_____________________________________________________________________________
def el_en_theta_tag():

    #electron generated energy and polar angle for electrons hitting the tagger

    #bins in log_10(theta)
    tbin = 0.001
    tmin = 0.0001
    tmax = 1

    #bins in energy
    ebin = 0.1
    emin = 3
    emax = 20

    #sel = "lowQ2s1_IsHit==1"
    #sel = "lowQ2s2_IsHit==1"
    sel = "ecal_IsHit==1"
    #gQ2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"

    can = ut.box_canvas()

    hEnThetaTag = ut.prepare_TH2D("hEnThetaTag", tbin, tmin, tmax, ebin, emin, emax)

    tree.Draw("el_gen:(TMath::Pi()-el_theta) >> hEnThetaTag", sel)

    ytit = "#it{E}_{e} / "+"{0:.1f} GeV".format(ebin)
    xtit = "#theta_{e} / "+"{0:.1f} rad".format(tbin)
    ut.put_yx_tit(hEnThetaTag, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.11)

    gPad.SetLogz()

    gPad.SetGrid()

    hEnThetaTag.SetMinimum(0.98)
    hEnThetaTag.SetContour(300)

    #hEnThetaTag.SetContour(10)
    hEnThetaTag.Draw("colz")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_en_theta_tag

#_____________________________________________________________________________
def evt_true_lQ2_lx():

    #generator true log_10(Q^2) and x

    lqbin = 5e-2
    #lqmin = -5
    lqmin = -10
    lqmax = 3

    #xbin = 0.01
    xbin = 0.1
    xmin = -12
    xmax = 0

    #Q2sel = "lowQ2s1_IsHit==1"
    #Q2sel = "lowQ2s2_IsHit==1"
    #Q2sel = "ecal_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"
    Q2sel = ""

    lQ2form = "TMath::Log10(true_Q2)"
    lxform = "TMath::Log10(true_x)"

    hLog10Q2xTag = ut.prepare_TH2D("hLog10Q2xTag", xbin, xmin, xmax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw(lQ2form+":"+lxform+" >> hLog10Q2xTag", Q2sel)
    #tree.Draw(lQ2form+":"+lxform+" >> hLog10Q2xTag")

    ytit = "log_{10}(#it{Q}^{2})"+" / {0:.3f}".format(lqbin)+" GeV^{2}"
    xtit = "log_{10}(#it{x})"+" / {0:.1f}".format(xbin)
    ut.put_yx_tit(hLog10Q2xTag, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.14)

    gPad.SetGrid()

    hLog10Q2xTag.Draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_true_lQ2_lx

#_____________________________________________________________________________
def evt_true_lx_ly():

    #generator true log_10(y) and log_10(x)

    xbin = 0.05 # 2e-2
    xmin = -12
    xmax = 0

    ybin = 0.02
    ymin = -4.5
    ymax = 0

    #Q2sel = "lowQ2s1_IsHit==1"
    #Q2sel = "lowQ2s2_IsHit==1"
    #Q2sel = "ecal_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"
    Q2sel = ""

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    can = ut.box_canvas()

    #tree.Draw("TMath::Log10(true_y):TMath::Log10(true_x) >> hXY")
    tree.Draw("TMath::Log10(true_y):TMath::Log10(true_x) >> hXY", Q2sel)

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_true_lx_ly

#_____________________________________________________________________________
def evt_true_lx_ly_lQ2():

    #generator distribution of true log_10(x), log_10(y) and log_10(Q^2)

    xbin = 0.1
    xmin = -12
    xmax = 0

    ybin = 0.05
    ymin = -4.5
    ymax = 0

    lqbin = 0.1
    lqmin = -8
    lqmax = 3

    #Q2sel = "lowQ2s1_IsHit==1"
    #Q2sel = "lowQ2s2_IsHit==1"
    #Q2sel = "ecal_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1"
    Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"
    #Q2sel = ""

    hXYQ2 = ut.prepare_TH3D("hXYQ2", xbin, xmin, xmax, ybin, ymin, ymax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw("TMath::Log10(true_Q2):TMath::Log10(true_y):TMath::Log10(true_x) >> hXYQ2", Q2sel)

    pXYQ2 = hXYQ2.Project3DProfile("yx")

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    pXYQ2.SetXTitle(xtit)
    pXYQ2.SetYTitle(ytit)
    pXYQ2.SetZTitle("log_{10}(#it{Q}^{2} (GeV^{2}))")
    pXYQ2.SetTitle("")

    pXYQ2.SetTitleOffset(1.3, "X")
    pXYQ2.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.16)

    gPad.SetGrid()

    pXYQ2.SetContour(300)
    pXYQ2.SetMinimum(lqmin)
    pXYQ2.SetMaximum(lqmax)

    pXYQ2.Draw("colz")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_true_lx_ly_lQ2

#_____________________________________________________________________________
def rel_true_Q2_el_Q2():

    #relative difference in true Q^2 and electron Q^2

    dbin = 0.01
    dmin = -2.1
    dmax = 1.1

    lqbin = 0.02
    #lqmin = -8 # taggers
    #lqmax = 0
    lqmin = -2.5 # ecal
    lqmax = 3

    #Q2sel = "lowQ2s1_IsHit==1"
    #Q2sel = "lowQ2s2_IsHit==1"
    Q2sel = "ecal_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"

    hRQ2 = ut.prepare_TH2D("hRQ2", lqbin, lqmin, lqmax, dbin, dmin, dmax)

    can = ut.box_canvas()

    Q2form = "(2*18*el_gen*(1-TMath::Cos(TMath::Pi()-el_theta)))"

    tree.Draw("(true_Q2-"+Q2form+")/true_Q2:TMath::Log10(true_Q2) >> hRQ2", Q2sel)

    ytit = "#frac{Q^{2} - Q^{2}_{e}}{Q^{2}}"
    xtit = "log_{10}(#it{Q}^{2})"#+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hRQ2, ytit, xtit, 1.8, 1.4)

    ut.set_margin_lbtr(gPad, 0.15, 0.11, 0.01, 0.11)

    hRQ2.Draw()

    hRQ2.SetMinimum(0.98)
    hRQ2.SetContour(300)

    gPad.SetGrid()

    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rel_true_Q2_el_Q2

#_____________________________________________________________________________
def evt_true_lQ2_lx_separate():

    #generator true log_10(Q^2) and x, separate for each detector

    lqbin = 0.1
    #lqmin = -5
    lqmin = -10
    lqmax = 3

    #xbin = 0.01
    xbin = 0.1
    xmin = -12
    xmax = 0

    #Q2sel = "lowQ2s1_IsHit==1"
    #Q2sel = "lowQ2s2_IsHit==1"
    #Q2sel = "ecal_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"
    #Q2sel = ""

    lQ2form = "TMath::Log10(true_Q2)"
    lxform = "TMath::Log10(true_x)"

    hLQ2xAll = ut.prepare_TH2D("hLQ2xAll", xbin*0.5, xmin, xmax, lqbin*0.5, lqmin, lqmax)
    hLQ2xS1 = ut.prepare_TH2D("hLQ2xS1", xbin, xmin, xmax, lqbin, lqmin, lqmax)
    hLQ2xS2 = ut.prepare_TH2D("hLQ2xS2", xbin, xmin, xmax, lqbin, lqmin, lqmax)
    hLQ2xEcal = ut.prepare_TH2D("hLQ2xEcal", xbin, xmin, xmax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw(lQ2form+":"+lxform+" >> hLQ2xAll")
    tree.Draw(lQ2form+":"+lxform+" >> hLQ2xS1", "lowQ2s1_IsHit==1")
    tree.Draw(lQ2form+":"+lxform+" >> hLQ2xS2", "lowQ2s2_IsHit==1")
    tree.Draw(lQ2form+":"+lxform+" >> hLQ2xEcal", "ecal_IsHit==1")

    ytit = "log_{10}(#it{Q}^{2})"#+" / {0:.3f}".format(lqbin)+" GeV^{2}"
    xtit = "log_{10}(#it{x})"#+" / {0:.1f}".format(xbin)
    ut.put_yx_tit(hLQ2xAll, ytit, xtit, 1.3, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.01, 0.01)

    gPad.SetGrid()

    hLQ2xAll.SetFillColor(rt.kRed-3)

    hLQ2xS1.SetFillColor(rt.kYellow)
    hLQ2xS2.SetFillColor(rt.kGreen)
    hLQ2xEcal.SetFillColor(rt.kBlue)

    hLQ2xAll.Draw("box")
    hLQ2xEcal.Draw("box same")
    hLQ2xS2.Draw("box same")
    hLQ2xS1.Draw("box same")

    leg = ut.prepare_leg(0.2, 0.78, 0.2, 0.18, 0.035)
    leg.AddEntry(hLQ2xAll, "All quasi-real electrons", "f")
    leg.AddEntry(hLQ2xS1, "Tagger 1", "f")
    leg.AddEntry(hLQ2xS2, "Tagger 2", "f")
    leg.AddEntry(hLQ2xEcal, "ECAL", "f")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_true_lQ2_lx_separate

#_____________________________________________________________________________
def evt_true_lx():

    #generated true log_10(x)

    xbin = 0.1
    xmin = -12
    xmax = 0

    lxform = "TMath::Log10(true_x)"

    hLxAll = ut.prepare_TH1D("hLxAll", xbin, xmin, xmax)

    can = ut.box_canvas()

    tree.Draw(lxform+" >> hLxAll")

    hLxAll.Draw("l")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_true_lx

#_____________________________________________________________________________
def evt_Q2_el_Q2():

    #comparison between true Q^2 and electron Q^2

    lqbin = 0.02
    lqmin = -10
    lqmax = 3
    #lqmin = -2.5 # ecal
    #lqmax = 3

    #Q2sel = "lowQ2s1_IsHit==1"
    #Q2sel = "lowQ2s2_IsHit==1"
    #Q2sel = "ecal_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1"
    #Q2sel = "lowQ2s1_IsHit==1 || lowQ2s2_IsHit==1 || ecal_IsHit==1"
    Q2sel = ""

    hQ2 = ut.prepare_TH2D("hQ2", lqbin, lqmin, lqmax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    Q2form = "(2*18*el_gen*(1-TMath::Cos(TMath::Pi()-el_theta)))"
    #Q2form = "gen_el_Q2" # from generator

    tree.Draw("TMath::Log10("+Q2form+"):TMath::Log10(true_Q2) >> hQ2", Q2sel)

    ytit = "Electron  log_{10}(#it{Q}^{2}_{e})"#+" / {0:.3f}".format(xbin)
    xtit = "Generator true  log_{10}(#it{Q}^{2})"#+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hQ2, ytit, xtit, 1.6, 1.4)

    ut.set_margin_lbtr(gPad, 0.12, 0.11, 0.03, 0.12)

    hQ2.Draw()

    hQ2.SetMinimum(0.98)
    hQ2.SetContour(300)

    gPad.SetGrid()

    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_Q2_el_Q2

#_____________________________________________________________________________
def evt_true_lQ2_ly_separate():

    #generator true log_10(Q^2) and y, separate for each detector

    lqbin = 0.2
    lqmin = -10
    lqmax = 3

    ybin = 0.1
    ymin = -5
    ymax = 0

    lQ2form = "TMath::Log10(true_Q2)"
    lyform = "TMath::Log10(true_y)"

    hLQ2yAll = ut.prepare_TH2D("hLQ2yAll", ybin*0.2, ymin, ymax, lqbin*0.2, lqmin, lqmax)
    #hLQ2yAll = ut.prepare_TH2D("hLQ2yAll", ybin, ymin, ymax, lqbin, lqmin, lqmax)
    hLQ2yS1 = ut.prepare_TH2D("hLQ2yS1", ybin, ymin, ymax, lqbin, lqmin, lqmax)
    hLQ2yS2 = ut.prepare_TH2D("hLQ2yS2", ybin, ymin, ymax, lqbin, lqmin, lqmax)
    hLQ2yEcal = ut.prepare_TH2D("hLQ2yEcal", ybin, ymin, ymax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw(lQ2form+":"+lyform+" >> hLQ2yAll")
    tree.Draw(lQ2form+":"+lyform+" >> hLQ2yS1", "lowQ2s1_IsHit==1")
    tree.Draw(lQ2form+":"+lyform+" >> hLQ2yS2", "lowQ2s2_IsHit==1")
    tree.Draw(lQ2form+":"+lyform+" >> hLQ2yEcal", "ecal_IsHit==1")

    ytit = "log_{10}(#it{Q}^{2})"#+" / {0:.3f}".format(lqbin)+" GeV^{2}"
    xtit = "log_{10}(#it{y})"#+" / {0:.1f}".format(xbin)
    ut.put_yx_tit(hLQ2yAll, ytit, xtit, 1.3, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.01, 0.01)

    gPad.SetGrid()

    hLQ2yAll.SetFillColor(rt.kRed-3)

    hLQ2yS1.SetFillColor(rt.kYellow)
    hLQ2yS2.SetFillColor(rt.kGreen)
    hLQ2yEcal.SetFillColor(rt.kBlue)

    hLQ2yAll.Draw("box")
    hLQ2yEcal.Draw("box same")
    hLQ2yS2.Draw("box same")
    hLQ2yS1.Draw("box same")

    leg = ut.prepare_leg(0.12, 0.78, 0.2, 0.18, 0.035)
    leg.AddEntry(hLQ2yAll, "All quasi-real electrons", "f")
    leg.AddEntry(hLQ2yS1, "Tagger 1", "f")
    leg.AddEntry(hLQ2yS2, "Tagger 2", "f")
    leg.AddEntry(hLQ2yEcal, "ECAL", "f")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_true_lQ2_ly_separate

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











    
