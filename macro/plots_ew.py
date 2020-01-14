#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath

import plot_utils as ut

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

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
if __name__ == "__main__":

    #infile = "../data/lmon.root"
    #infile = "../data/lmon_18x275_ewV1_flat_10Mevt.root"
    #infile = "../data/lmon_18x275_ewV1_tilt_10Mevt.root"
    infile = "../data/lmon_18x275_ewV2_10Mevt.root"

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 3
    funclist = []
    funclist.append( ew_xy ) # 0
    funclist.append( ew_z ) # 1
    funclist.append( ew_conv_theta ) # 2
    funclist.append( ew_conv_phi ) # 3

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #call the plot function
    funclist[iplot]()


















