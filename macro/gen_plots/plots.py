#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import configparser

import sys
sys.path.append('/home/jaroslav/sim/GETaLM/models')
sys.path.append('/home/jaroslav/sim/GETaLM/base')
from gen_zeus import gen_zeus
from gen_h1 import gen_h1

sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def plot_delta():

    #photon delta

    dbin = 1
    dmin = 0
    dmax = 110

    can = ut.box_canvas()

    hD = ut.prepare_TH1D("hD", dbin, dmin, dmax)

    tree.Draw("phot_delta >> hD")

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.01)

    hD.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_delta

#_____________________________________________________________________________
def plot_w():

    #photon w

    wbin = 10
    wmin = 0
    wmax = 12000

    can = ut.box_canvas()

    hW = ut.prepare_TH1D("hW", wbin, wmin, wmax)

    tree.Draw("phot_w >> hW")

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.01)

    hW.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_w

#_____________________________________________________________________________
def plot_w_delta():

    #photon w and delta

    wbin = 0.02
    wmin = 1
    wmax = 4

    dbin = 0.02
    dmax = 2.5

    can = ut.box_canvas()

    hWD = ut.prepare_TH2D("hWD", dbin, 0, dmax, wbin, wmin, wmax)

    #tree.Draw("phot_w:phot_delta >> hWD") # y:x
    tree.Draw("TMath::Log10(phot_w):TMath::Log10(phot_delta) >> hWD") # y:x

    hWD.SetXTitle("log(#delta)")
    hWD.SetYTitle("log(w)")

    hWD.SetTitleOffset(1.6, "Y")
    hWD.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.13)

    hWD.SetMinimum(0.98)
    hWD.SetContour(300)

    #gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_w_delta

#_____________________________________________________________________________
def plot_dSigDe_all():

    # dSigma / dEgamma over all energies, ZEUS parametrization

    parse = ConfigParser.RawConfigParser()
    parse.add_section("main")
    parse.set("main", "emin", "0.1") # GeV

    parse.set("main", "Ee", "18")
    parse.set("main", "Ep", "275")
    sig_top = gen_zeus(parse).dSigDe

    parse.set("main", "Ee", "10")
    parse.set("main", "Ep", "110")
    sig_mid = gen_zeus(parse).dSigDe

    parse.set("main", "Ee", "5")
    parse.set("main", "Ep", "41")
    sig_low = gen_zeus(parse).dSigDe

    gStyle.SetPadTickY(1)
    can = ut.box_canvas()

    frame = gPad.DrawFrame(0.1, 1, 19, 80)
    frame.Draw()

    ut.set_F1(sig_top)
    ut.set_F1(sig_mid, rt.kYellow+1)
    ut.set_F1(sig_low, rt.kBlue)

    sig_top.Draw("same")
    sig_mid.Draw("same")
    sig_low.Draw("same")

    ytit = "d#sigma / d#it{E}_{#gamma} (mb/GeV)"
    xtit = "#it{E}_{#gamma} (GeV)"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.4)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.01, 0.01)

    frame.GetYaxis().SetMoreLogLabels()

    leg = ut.prepare_leg(0.65, 0.77, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(sig_top, "18 #times 275 GeV", "l")
    leg.AddEntry(sig_mid, "10 #times 100 GeV", "l")
    leg.AddEntry(sig_low, "5 #times 41 GeV", "l")
    leg.Draw("same")

    gPad.SetLogy()

    gPad.SetGrid()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#plot_dSigDe_all

#_____________________________________________________________________________
def plot_el_en():

    #scattered electron energy

    ebin = 0.1
    emin = 0
    emax = 20

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("el_en >> hE")

    hE.SetYTitle("Events / ({0:.3f}".format(ebin)+" GeV)")
    hE.SetXTitle("#it{E}_{e} (GeV)")

    hE.SetTitleOffset(1.9, "Y")
    hE.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.01)

    #hE.GetYaxis().SetMoreLogLabels()

    hE.Draw()

    #gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_vxy():

    #vertex position of generated photon along x and y

    xbin = 0.01
    ybin = 0.001

    xmin = -1.5
    xmax = 1.5

    ymin = -0.2
    ymax = 0.2

    can = ut.box_canvas()

    hV = ut.prepare_TH2D("hV", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("beff_vy:beff_vx >> hV")

    hV.SetXTitle("#it{x} of primary vertex (mm)")
    hV.SetYTitle("#it{y} of primary vertex (mm)")

    hV.SetTitleOffset(1.6, "Y")
    hV.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.13)

    #gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_vxy

#_____________________________________________________________________________
def plot_theta_SigTheta():

    #distribution in theta and parametrization

    tbin = 1e-5
    tmax = 1.5e-3
    #tbin = 1e-2
    #tmax = 1.5

    can = ut.box_canvas()

    ht = ut.prepare_TH1D("ht", tbin, 0, tmax)

    tree.Draw("(TMath::Pi()-phot_theta) >> ht")
    #tree.Draw("(TMath::Pi()-phot_theta)*1e3 >> ht")

    #theta parametrization
    parse = ConfigParser.RawConfigParser()
    parse.add_section("main")
    parse.set("main", "emin", "0.5")
    parse.set("main", "Ee", "18")
    parse.set("main", "Ep", "275")

    gen = gen_zeus(parse)
    tpar = gen.dSigDtheta
    tpar.SetNpx(600)
    tpar.SetLineWidth(3)

    #scale the parametrization to the plot
    norm = tbin * ht.Integral() / tpar.Integral(0, tmax)
    print("norm:", norm)
    gen.theta_const = norm * gen.theta_const

    ht.SetYTitle("Events / ({0:.3f}".format(tbin*1e3)+" mrad)")
    ht.SetXTitle("#theta_{\gamma} (rad)")

    ht.SetTitleOffset(1.5, "Y")
    ht.SetTitleOffset(1.2, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.08)

    ht.Draw()

    ht.SetMaximum(5e6)

    tpar.Draw("same")

    leg = ut.prepare_leg(0.37, 0.84, 0.2, 0.08, 0.035)
    leg.AddEntry(tpar, "Bethe-Heitler parametrization", "l")
    leg.AddEntry(ht, "Angular divergence applied", "lp")
    leg.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_vz():

    #vertex position of generated photon along x or y

    vbin = 0.8
    vmin = -80
    vmax = 80

    can = ut.box_canvas()

    hV = ut.prepare_TH1D("hV", vbin, vmin, vmax)

    tree.Draw("beff_vz >> hV")

    hV.SetYTitle("Events / ({0:.3f}".format(vbin)+" mm)")
    hV.SetXTitle("z vertex (mm)")

    hV.SetTitleOffset(1.6, "Y")
    hV.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.05, 0.02)

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_vz

#_____________________________________________________________________________
def plot_vx():

    #vertex position of generated photon along x or y

    vbin = 0.1
    vmin = -10
    vmax = 10

    can = ut.box_canvas()

    hV = ut.prepare_TH1D("hV", vbin, vmin, vmax)

    tree.Draw("beff_vx >> hV")
    #tree.Draw("beff_vy >> hV")

    hV.SetYTitle("Events / ({0:.3f}".format(vbin)+" mm)")
    hV.SetXTitle("x vertex (mm)")
    #hV.SetXTitle("y vertex (mm)")

    hV.SetTitleOffset(1.9, "Y")
    hV.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.02)

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_vx

#_____________________________________________________________________________
def plot_dSigDtheta():

    # dSigma / dTheta according to ZEUS parametrization

    parse = ConfigParser.RawConfigParser()
    parse.add_section("main")
    parse.set("main", "emin", "6")
    parse.set("main", "Ee", "18")
    parse.set("main", "Ep", "275")

    gen = gen_zeus(parse)
    sig = gen.dSigDtheta

    can = ut.box_canvas()

    sig.SetLineWidth(3)
    sig.SetNpx(1000)
    sig.SetTitle("")
    sig.Draw()

    sig.GetXaxis().SetTitle("#theta_{#gamma} (rad)")
    sig.GetYaxis().SetTitle("a. u.")

    sig.GetYaxis().SetTitleOffset(1.5)
    sig.GetXaxis().SetTitleOffset(1.3)

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.08)

    leg = ut.prepare_leg(0.58, 0.78, 0.24, 0.15, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(sig, "#frac{d#sigma}{d#theta_{#gamma}}", "l")
    leg.AddEntry(None, "E_{e} = 18 GeV", "")
    leg.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_theta():

    #polar angle of generated photons

    tbin = 0.01
    tmax = 4

    can = ut.box_canvas()

    ht = ut.prepare_TH1D("ht", tbin, 0, tmax)

    tree.Draw("(TMath::Pi()-phot_theta)*1000 >> ht")

    #ht.SetYTitle("Events / ({0:.3f}".format(tbin)+" mrad)")
    ht.SetYTitle("Counts")
    ht.SetXTitle("Photon #it{#theta} (mrad)")

    ht.SetTitleOffset(1.5, "Y")
    ht.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.025)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.11)

    gPad.SetGrid()

    ht.Draw()

    #leg = ut.prepare_leg(0.2, 0.87, 0.18, 0.08, 0.035)
    #leg.AddEntry(None, "Angular distribution of Bethe-Heitler photons", "")
    #leg.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_en():

    #energy distribution of generated photons

    ebin = 0.1
    emin = 4
    emax = 28

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("phot_en >> hE")

    hE.SetYTitle("Events / ({0:.3f}".format(ebin)+" GeV)")
    hE.SetXTitle("#it{E}_{#gamma} (GeV)")

    hE.SetTitleOffset(1.9, "Y")
    hE.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.01)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.14)

    hE.GetYaxis().SetMoreLogLabels()

    hE.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_dSigDy():

    # dSigma / dy according to H1 parametrization

    parse = ConfigParser.RawConfigParser()
    parse.add_section("main")
    parse.set("main", "emin", "6")
    parse.set("main", "Ee", "27.6")
    parse.set("main", "Ep", "920")

    gen = gen_h1(parse)
    sig = gen.dSigDy

    can = ut.box_canvas()

    sig.SetNpx(300)
    sig.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_dSigDe():

    # dSigma / dEgamma according to ZEUS parametrization

    parse = ConfigParser.RawConfigParser()
    parse.add_section("main")
    parse.set("main", "emin", "6")
    parse.set("main", "Ee", "18")
    parse.set("main", "Ep", "275")
    gen = gen_zeus(parse)
    sig = gen.dSigDe

    gStyle.SetPadTickY(1)
    can = ut.box_canvas()

    #frame = gPad.DrawFrame(6, 0, 29, 6)
    frame = gPad.DrawFrame(5, 0, 19, 7.2)

    sig.SetLineWidth(3)
    sig.SetNpx(1000)
    sig.SetTitle("")
    sig.Draw("same")

    frame.GetXaxis().SetTitle("#it{E}_{#gamma} (GeV)")
    frame.GetYaxis().SetTitle("d#sigma / d#it{E}_{#gamma} (mb/GeV)")

    frame.GetYaxis().SetTitleOffset(1.1)
    frame.GetXaxis().SetTitleOffset(1.3)

    frame.SetTickLength(0.015, "X")
    frame.SetTickLength(0.015, "Y")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.01)
    gPad.SetLeftMargin(0.09)

    leg = ut.prepare_leg(0.65, 0.73, 0.24, 0.2, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(sig, "#frac{d#sigma}{d#it{E}_{#gamma}}", "l")
    leg.AddEntry(None, "", "")
    #leg.AddEntry(None, "#it{E}_{e} = 27.6 GeV", "")
    #leg.AddEntry(None, "#it{E}_{p} = 920 GeV", "")
    leg.AddEntry(None, "#it{E}_{e} = 18 GeV", "")
    leg.AddEntry(None, "#it{E}_{p} = 275 GeV", "")
    leg.Draw("same")

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
if __name__ == "__main__":

    #basedir = "/home/jaroslav/sim/lgen/data"
    basedir = "/home/jaroslav/sim/lattice/gen/"

    #infile = "lgen_18x275_beff2_10p1Mevt.root"
    #infile = "lgen_18x275_Lif_0p1GeV_5Mevt.root"
    #infile = "lgen_18x275_Au_Lif_0p1GeV_5Mevt.root"
    #infile = "lgen_zeus_10g.root"
    infile = "lgen_Lif_10g.root"

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 3
    funclist = []
    funclist.append( plot_dSigDe ) # 0
    funclist.append( plot_dSigDy ) # 1
    funclist.append( plot_en ) # 2
    funclist.append( plot_theta ) # 3
    funclist.append( plot_dSigDtheta ) # 4
    funclist.append( plot_vx ) # 5
    funclist.append( plot_vz ) # 6
    funclist.append( plot_theta_SigTheta ) # 7
    funclist.append( plot_vxy ) # 8
    funclist.append( plot_el_en ) # 9
    funclist.append( plot_dSigDe_all ) # 10
    funclist.append( plot_w_delta ) # 11
    funclist.append( plot_w ) # 12
    funclist.append( plot_delta ) # 13

    #open the input
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("ltree")

    #call the plot function
    funclist[iplot]()




















