#!/usr/bin/python

#comparison between version 1 and version 2 of photon exit window

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath, TGraphAsymmErrors

import plot_utils as ut

#_____________________________________________________________________________
def conv_phi():

    #conversion probablity as a function of azimuthal angle phi

    pbin = 0.4
    pmin = -TMath.Pi()-0.3
    pmax = TMath.Pi()+0.3

    prec = 0.01
    delt = 1e-6

    gROOT.LoadMacro("get_ew_conv.C")
    hEffV1 = rt.get_ew_conv(tree_v1, "phot_phi", "ew_conv", prec, delt)
    hEffV2 = rt.get_ew_conv(tree_v2, "phot_phi", "ew_conv", prec, delt)

    #hEffV1 = get_eff(tree_v1, "phot_phi", "ew_conv", pbin, pmin, pmax)
    #hEffV2 = get_eff(tree_v2, "phot_phi", "ew_conv", pbin, pmin, pmax)

    ut.set_graph(hEffV1, rt.kBlue)
    ut.set_graph(hEffV2, rt.kRed, rt.kFullTriangleUp)
    hEffV2.SetMarkerSize(1.5)

    #plot the probability
    can = ut.box_canvas()

    #frame = gPad.DrawFrame(pmin, 0.075, pmax, 0.087)
    frame = gPad.DrawFrame(pmin, 0.065, pmax, 0.095)

    frame.SetXTitle("Generated #phi (rad)")
    frame.SetYTitle("Conversion probability")

    frame.SetTitleOffset(2.1, "Y")
    frame.SetTitleOffset(1.2, "X")

    ut.set_margin_lbtr(gPad, 0.14, 0.09, 0.02, 0.01)

    frame.Draw()

    hEffV1.Draw("psame")
    hEffV2.Draw("psame")

    leg = ut.prepare_leg(0.2, 0.84, 0.2, 0.1, 0.035)
    leg.AddEntry(hEffV1, "Tilted plane", "lp")
    leg.AddEntry(hEffV2, "Half-cylinder", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def conv_theta():

    #conversion probablity as a function of polar angle theta

    tbin = 2e-4
    tmin = 0
    tmax = 2.5e-3

    prec = 0.01
    delt = 1e-6

    gROOT.LoadMacro("get_ew_conv.C")
    hEffV1 = rt.get_ew_conv(tree_v1, "phot_theta", "ew_conv", prec, delt, -1., TMath.Pi())
    hEffV2 = rt.get_ew_conv(tree_v2, "phot_theta", "ew_conv", prec, delt, -1., TMath.Pi())

    #hEffV1 = get_eff(tree_v1, "TMath::Pi()-phot_theta", "ew_conv", tbin, tmin, tmax)
    #hEffV2 = get_eff(tree_v2, "TMath::Pi()-phot_theta", "ew_conv", tbin, tmin, tmax)

    ut.set_graph(hEffV1, rt.kBlue)
    ut.set_graph(hEffV2, rt.kRed, rt.kFullTriangleUp)
    hEffV2.SetMarkerSize(1.5)

    #plot the probability
    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0.065, tmax, 0.095)

    frame.SetXTitle("Generated #vartheta (rad)")
    frame.SetYTitle("Conversion probability")

    frame.SetTitleOffset(2.1, "Y")
    frame.SetTitleOffset(1.5, "X")

    ut.set_margin_lbtr(gPad, 0.14, 0.11, 0.02, 0.01)

    frame.Draw()

    hEffV1.Draw("psame")
    hEffV2.Draw("psame")

    leg = ut.prepare_leg(0.2, 0.84, 0.2, 0.1, 0.035)
    leg.AddEntry(hEffV1, "Tilted plane", "lp")
    leg.AddEntry(hEffV2, "Half-cylinder", "lp")
    leg.Draw("same")

    gPad.SetLogx()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def get_eff(tree, draw, match, xbin, xmin, xmax):

    #efficiency calculation, fixed bins

    hAll = ut.prepare_TH1D("hAll", xbin, xmin, xmax)
    hSel = ut.prepare_TH1D("hSel", xbin, xmin, xmax)

    tree.Draw(draw+" >> hAll")
    tree.Draw(draw+" >> hSel", match+" == 1")

    #output efficiency distribution
    hEff = TGraphAsymmErrors(hSel, hAll)

    return hEff


#_____________________________________________________________________________
if __name__ == "__main__":

    in_v1 = "../data/lmon_18x275_ewV1_tilt_10Mevt.root" # version 1
    in_v2 = "../data/lmon_18x275_ewV2_10Mevt.root" # version 2

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 1
    funclist = []
    funclist.append( conv_theta ) # 0
    funclist.append( conv_phi ) # 1

    #inputs on v1 and v2
    inp_v1 = TFile.Open(in_v1)
    tree_v1 = inp_v1.Get("DetectorTree")
    inp_v2 = TFile.Open(in_v2)
    tree_v2 = inp_v2.Get("DetectorTree")

    #call the plot function
    funclist[iplot]()


















