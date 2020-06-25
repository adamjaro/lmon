#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath, TF1

import ConfigParser

import plot_utils as ut

#_____________________________________________________________________________
def phot_theta():

    #generated photon polar angle

    tbin = 1e-5
    tmin = 0
    tmax = 2e-3

    can = ut.box_canvas()

    hT = ut.prepare_TH1D("hT", tbin, tmin, tmax)

    tree.Draw("(TMath::Pi()-phot_theta) >> hT")

    print "Entries:", hT.GetEntries()

    #theta parametrization
    parse = ConfigParser.RawConfigParser()
    parse.add_section("lgen")
    parse.set("lgen", "emin", "1") # GeV
    parse.set("lgen", "tmax", "0.002")

    import sys
    sys.path.append('/home/jaroslav/sim/eic-lgen/')
    from gen_zeus import gen_zeus
    gen = gen_zeus(18, 275, parse) # Ee, Ep, GeV
    tpar = gen.dSigDtheta
    tpar.SetNpx(600)
    tpar.SetLineWidth(3)

    #scale the parametrization to the plot
    norm = tbin * hT.Integral() / tpar.Integral(0, tmax)
    print "norm:", norm
    gen.theta_const = norm * gen.theta_const

    ut.put_yx_tit(hT, "Events", "#theta_{#gamma} (rad)", 1.5, 1.2)

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.08)

    hT.SetMaximum(6e5)

    hT.Draw()

    tpar.Draw("same")

    gPad.SetLogy()

    leg = ut.prepare_leg(0.37, 0.84, 0.2, 0.08, 0.035)
    leg.AddEntry(tpar, "Bethe-Heitler parametrization", "l")
    leg.AddEntry(hT, "Angular divergence applied", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phot_theta

#_____________________________________________________________________________
def ew_efrac():

    #fraction of energy carried by electron or positron

    #ebin = 1e-2
    nbins = 100
    emin = 0
    emax = 1

    can = ut.box_canvas()

    #hE = ut.prepare_TH1D("hE", ebin, emin, emax)
    hE = ut.prepare_TH1D_n("hE", nbins, emin, emax)

    tree.Draw("ew_enPos/(phot_gen*1e3) >> hE", "ew_conv==1")
    #tree.Draw("ew_enEl/(phot_gen*1e3) >> hE", "ew_conv==1")

    #frame = gPad.DrawFrame(0, 400, 1, 1300)
    frame = gPad.DrawFrame(0, 4000, 1, 13000)
    frame.Draw()

    xtit = "#it{z} = #it{E}_{+}/#it{E}_{#gamma}"
    ut.put_yx_tit(frame, "d#it{N}/d#it{z}", xtit, 1.8, 1.2)

    #ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.02, 0.02)
    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.04, 0.02)

    hE.Draw("e1same")

    #QED parametrization
    dSigDz = TF1("dSigDz", eq_94p5_z, 0, 1, 2)
    dSigDz.SetParameter(0, 10)
    dSigDz.SetParameter(1, 1)
    dSigDz.SetNpx(300)
    dSigDz.SetLineWidth(3)

    #normalize the parametrization
    norm = hE.GetBinWidth(1) * hE.Integral() / dSigDz.Integral(1e-4, 1-1e-4)
    dSigDz.SetParameter(1, norm)

    dSigDz.Draw("same")

    leg = ut.prepare_leg(0.2, 0.78, 0.2, 0.14, 0.035)
    leg.AddEntry(None, "#it{E}_{#gamma} = 10 GeV", "")
    leg.AddEntry(dSigDz, "QED approximation", "l")
    leg.AddEntry(hE, "Geant4 simulation", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#ew_efrac

#_____________________________________________________________________________
def eq_94p5_z(val, par):

    # Berestetskii, Lifshitz and Pitaevskii, QED, page 411, eq. 94.5 in z = Ep/w

    w = par[0]
    z = val[0]

    norm = par[1]

    sig = z**2 + (1.-z)**2 + z*(1.-z)*2./3

    m = 0.000511
    sig *= TMath.Log( (2.*w*z*(1.-z))/m - 0.5 )

    return sig*norm

#eq_94p5_z

#_____________________________________________________________________________
def ew_econv():

    #difference between sum of electron and positron energy and photon energy

    ebin = 1e-6
    emin = -1e-3
    emax = 1e-3

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("(ew_enEl+ew_enPos)-(phot_gen*1e3) >> hE", "ew_conv==1")

    #hZ.SetXTitle("#it{z} of conversion point (meter)")
    #hZ.SetYTitle("Events / ({0:.3f} m)".format(zbin))

    #hZ.SetTitleOffset(1.5, "Y")
    #hZ.SetTitleOffset(1.2, "X")

    #ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.03)

    hE.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#ew_econv

#_____________________________________________________________________________
def ew_conv_phi():

    #conversion probablity as a function of azimuthal angle phi

    pbin = 0.4
    pmin = -TMath.Pi()-0.3
    pmax = TMath.Pi()+0.3

    can = ut.box_canvas()

    hPhiAll = ut.prepare_TH1D("hPhiAll", pbin, pmin, pmax)
    hPhiSel = ut.prepare_TH1D("hPhiSel", pbin, pmin, pmax)

    tree.Draw("phot_phi >> hPhiAll")
    tree.Draw("phot_phi >> hPhiSel", "ew_conv == 1")

    print "Entries all:", hPhiAll.GetEntries()
    print "Entries sel:", hPhiSel.GetEntries()

    hConvPhi = hPhiSel.Clone()
    hConvPhi.Sumw2()
    hConvPhi.Divide(hPhiAll)

    hConvPhi.SetXTitle("Generated #phi (rad)")
    hConvPhi.SetYTitle("Conversion probability / ({0:.3} rad)".format(pbin))

    hConvPhi.SetTitleOffset(2.1, "Y")
    hConvPhi.SetTitleOffset(1.2, "X")

    ut.set_margin_lbtr(gPad, 0.15, 0.09, 0.02, 0.01)

    #hPhiAll.Draw()
    #hPhiSel.Draw()
    hConvPhi.Draw()

    hConvPhi.SetMinimum(0.075) # for flat
    hConvPhi.SetMaximum(0.087)

    #hConvPhi.SetMinimum(0.19) # for tilt
    #hConvPhi.SetMaximum(0.24)

    leg = ut.prepare_leg(0.2, 0.84, 0.2, 0.08, 0.035)
    #leg.AddEntry(hConvPhi, "Flat exit window", "lp")
    leg.AddEntry(hConvPhi, "Tilted exit window", "lp")
    leg.Draw("same")

    #gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def ew_conv_theta():

    #conversion probablity as a function of polar angle theta

    tbin = 2e-4
    tmin = 0
    tmax = 1.8e-3

    can = ut.box_canvas()

    hTall = ut.prepare_TH1D("hTall", tbin, tmin, tmax)
    hTsel = ut.prepare_TH1D("hTsel", tbin, tmin, tmax)

    tree.Draw("TMath::Pi()-phot_theta >> hTall")
    tree.Draw("TMath::Pi()-phot_theta >> hTsel", "ew_conv == 1")

    print "Entries all:", hTall.GetEntries()
    print "Entries sel:", hTsel.GetEntries()

    hConvTheta = hTsel.Clone()
    hConvTheta.Sumw2()
    hConvTheta.Divide(hTall)

    hConvTheta.SetXTitle("Generated #vartheta, including divergence (rad)")
    hConvTheta.SetYTitle("Conversion probability / ({0:.3} mrad)".format(tbin*1e3))

    hConvTheta.SetTitleOffset(1.7, "Y")
    hConvTheta.SetTitleOffset(1.2, "X")

    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.02, 0.08)

    #hTall.Draw()
    #hTsel.Draw()
    hConvTheta.Draw()

    hConvTheta.SetMinimum(0.04) # for flat
    hConvTheta.SetMaximum(0.14)

    #hConvTheta.SetMinimum(0.03) # for tilt
    #hConvTheta.SetMaximum(0.37)

    leg = ut.prepare_leg(0.2, 0.84, 0.2, 0.08, 0.035)
    #leg.AddEntry(hConvTheta, "Flat exit window", "lp")
    leg.AddEntry(hConvTheta, "Tilted exit window", "lp")
    leg.Draw("same")

    #gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def ew_z():

    #photon impact point along z

    zbin = 0.004
    #zmin = -22.5
    #zmax = -20
    zmin = -22.5
    zmax = -20

    can = ut.box_canvas()

    hZ = ut.prepare_TH1D("hZ", zbin, zmin, zmax)

    #tree.Draw("ew_photZ/1000. >> hZ") # , "ew_photZ>9998." only 9 events out of 1e6
    tree.Draw("ew_convZ/1e3 >> hZ", "ew_conv==1")

    print "Entries:", hZ.GetEntries()

    hZ.SetXTitle("#it{z} of conversion point (meter)")
    hZ.SetYTitle("Events / ({0:.3f} m)".format(zbin))

    hZ.SetTitleOffset(1.5, "Y")
    hZ.SetTitleOffset(1.2, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.03)

    hZ.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def ew_xy():

    #photon impact point in xy

    xbin = 1
    xmin = -50
    xmax = 50

    can = ut.box_canvas()

    hX = ut.prepare_TH2D("hX", xbin, xmin, xmax, xbin, xmin, xmax)

    tree.Draw("ew_photY:ew_photX >> hX")#, "phot_en<1000")

    hX.SetXTitle("#it{x} on exit window (mm)")
    hX.SetYTitle("#it{y} on exit window (mm)")

    hX.GetXaxis().CenterTitle()
    hX.GetYaxis().CenterTitle()

    hX.SetTitleOffset(1.4, "Y")
    hX.SetTitleOffset(1.2, "X")

    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.02, 0.11)

    hX.Draw()

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
if __name__ == "__main__":

    #infile = "../data/lmon.root"
    #infile = "../data/test/lmon.root"
    #infile = "../data/lmon_18x275_ewV1_flat_10Mevt.root"
    #infile = "../data/lmon_18x275_ewV1_tilt_10Mevt.root"
    #infile = "../data/lmon_18x275_ewV2_10Mevt.root"
    #infile = "../data/lmon_10GeV_ewV2_1Mevt.root"
    #infile = "../data/lmon_10GeV_ewV2_10Mevt.root"
    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_1Mevt.root"
    infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_NoFilter_1Mevt.root"

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 6
    funclist = []
    funclist.append( ew_xy ) # 0
    funclist.append( ew_z ) # 1
    funclist.append( ew_conv_theta ) # 2
    funclist.append( ew_conv_phi ) # 3
    funclist.append( ew_econv ) # 4
    funclist.append( ew_efrac ) # 5
    funclist.append( phot_theta ) # 6

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #call the plot function
    funclist[iplot]()


















