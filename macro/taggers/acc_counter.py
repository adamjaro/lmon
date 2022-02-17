#!/usr/bin/python3

from ctypes import c_double, c_bool

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree
from ROOT import std

#from EventStore import EventStore

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 9

    func = {}
    func[0] = acc_en_s12
    func[1] = acc_lQ2_s12
    func[2] = acc_theta_s12
    func[3] = acc_eta_s12
    func[4] = acc_en_theta
    func[5] = acc_en_eta
    func[6] = acc_ly_lx
    func[7] = acc_pitheta_s12
    func[8] = acc_mlt_theta_s12
    func[9] = acc_en_pitheta
    func[10] = acc_lQ2_en
    func[11] = acc_lQ2_pitheta
    func[12] = hit_en

    func[101] = load_lmon
    func[102] = load_dd

    func[iplot]()

#main

#_____________________________________________________________________________
def acc_en_s12():

    #acceptance in energy for Tagger 1 by lmon and dd4hep

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag2a/hits_tag_10files.root"

    infile = TFile.Open(inp)
    tree_lmon = infile.Get("event")

    #inp_dd = TFile.Open("dd.root")
    #tree_dd = inp_dd.Get("event")

    emin = 2
    emax = 19

    #amax = 0.6
    amax = 0.9

    acc_lmon_s1 = rt.acc_Q2_kine(tree_lmon, "true_el_E", "s1_IsHit")
    acc_lmon_s1.prec = 0.05
    acc_lmon_s1.bmin = 0.1
    #acc_lmon_s1.nev = int(1e5)
    gLmonS1 = acc_lmon_s1.get()

    acc_lmon_s2 = rt.acc_Q2_kine(tree_lmon, "true_el_E", "s2_IsHit")
    acc_lmon_s2.prec = 0.05
    acc_lmon_s2.bmin = 0.1
    #acc_lmon_s2.nev = int(1e5)
    gLmonS2 = acc_lmon_s2.get()

    #acc_dd = rt.acc_Q2_kine(tree_dd, "gen_en", "s1_IsHit")
    #acc_dd = rt.acc_Q2_kine(tree_dd, "gen_en", "s2_IsHit")
    #acc_dd.prec = 0.1
    #acc_dd.bmin = 0.1
    #gDD = acc_dd.get()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, 0, emax, amax)

    ut.put_yx_tit(frame, "Tagger acceptance", "Electron energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gLmonS1, rt.kRed)
    gLmonS1.Draw("psame")

    ut.set_graph(gLmonS2, rt.kBlue)
    gLmonS2.Draw("psame")

    #ut.set_graph(gDD, rt.kRed)
    #gDD.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.82, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(gLmonS1, "Tagger 1", "lp")
    leg.AddEntry(gLmonS2, "Tagger 2", "lp")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_s12

#_____________________________________________________________________________
def acc_lQ2_s12():

    #acceptance in log_10(Q^2) for tagger 1 and tagger 2

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    lQ2min = -9
    lQ2max = 0

    #amax = 0.21
    amax = 0.4

    as1 = rt.acc_Q2_kine(tree, "true_Q2", "s1_IsHit")
    as1.modif = 1 # log_10(Q^2) from Q2
    as1.prec = 0.05
    as1.bmin = 0.1
    as1.nev = int(1e5)
    gs1 = as1.get()

    as2 = rt.acc_Q2_kine(tree, "true_Q2", "s2_IsHit")
    as2.modif = 1 # log_10(Q^2) from Q2
    as2.prec = 0.05
    as2.bmin = 0.1
    as2.nev = int(1e5)
    gs2 = as2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(lQ2min, 0, lQ2max, amax)
    ut.put_yx_tit(frame, "Tagger acceptance", "Virtuality #it{Q}^{2} (GeV^{2})", 1.6, 1.5)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.11, 0.03, 0.02)

    #labels in power of 10
    ax = frame.GetXaxis()
    labels = range(lQ2min, lQ2max+1, 1)
    for i in range(len(labels)):
        if labels[i] == 0:
            ax.ChangeLabel(i+1, -1, -1, -1, -1, -1, "1")
            continue
        ax.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")
    ax.SetLabelOffset(0.015)

    ut.set_graph(gs1, rt.kRed)
    gs1.Draw("psame")

    ut.set_graph(gs2, rt.kBlue)
    gs2.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.82, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(gs1, "Tagger 1", "lp")
    leg.AddEntry(gs2, "Tagger 2", "lp")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_lQ2_s12

#_____________________________________________________________________________
def acc_theta_s12():

    #acceptance in electron polar angle for tagger 1 and tagger 2

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    tmin = TMath.Pi() - 1.1e-2
    tmax = TMath.Pi() + 1e-3

    #amax = 0.25
    amax = 0.4

    as1 = rt.acc_Q2_kine(tree, "true_el_theta", "s1_IsHit")
    as1.prec = 0.1
    as1.bmin = 2e-4
    #as1.nev = int(1e5)
    gs1 = as1.get()

    as2 = rt.acc_Q2_kine(tree, "true_el_theta", "s2_IsHit")
    as2.prec = 0.1
    as2.bmin = 2e-4
    #as2.nev = int(1e5)
    gs2 = as2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0, tmax, amax)
    ut.put_yx_tit(frame, "Tagger acceptance", "Electron polar angle #it{#theta} (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gs1, rt.kRed)
    gs1.Draw("psame")

    ut.set_graph(gs2, rt.kBlue)
    gs2.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.82, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(gs1, "Tagger 1", "lp")
    leg.AddEntry(gs2, "Tagger 2", "lp")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_theta_s12

#_____________________________________________________________________________
def acc_eta_s12():

    #acceptance in electron pseudorapidity for tagger 1 and tagger 2

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    emin = -17
    emax = -3

    amax = 0.3

    as1 = rt.acc_Q2_kine(tree, "true_el_theta", "s1_IsHit")
    as1.modif = 0 # eta from theta
    as1.prec = 0.01
    as1.bmin = 0.1
    #as1.nev = int(1e5)
    gs1 = as1.get()

    as2 = rt.acc_Q2_kine(tree, "true_el_theta", "s2_IsHit")
    as2.modif = 0 # eta from theta
    as2.prec = 0.01
    as2.bmin = 0.1
    #as2.nev = int(1e5)
    gs2 = as2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, 0, emax, amax)
    ut.put_yx_tit(frame, "Acceptance", "Electron pseudorapidity #eta", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gs1, rt.kBlue)
    gs1.Draw("psame")

    ut.set_graph(gs2, rt.kRed)
    gs2.Draw("psame")

    gPad.SetGrid()

    #leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry(None, "Tagger 1", "")
    #leg.AddEntry(glQ2Py, "Pythia6", "l")
    #leg.AddEntry(glQ2Qr, "QR", "l")
    #leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_eta_s12

#_____________________________________________________________________________
def acc_en_theta():

    #2D acceptance in energy and polar angle theta

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"

    #bins in theta
    tbin = 2e-4
    tmin = TMath.Pi() - 1.1e-2
    tmax = TMath.Pi() + 1e-3

    #bins in energy
    ebin = 0.3
    emin = 0
    emax = 20

    #tagger 1 or 2
    tag = 1

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 0:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

    can = ut.box_canvas()

    hEnThetaTag = ut.prepare_TH2D("hEnThetaTag", tbin, tmin, tmax, ebin, emin, emax)
    hEnThetaAll = ut.prepare_TH2D("hEnThetaAll", tbin, tmin, tmax, ebin, emin, emax)

    form = "true_el_E:true_el_theta"
    tree.Draw(form+" >> hEnThetaTag", sel)
    tree.Draw(form+" >> hEnThetaAll")

    hEnThetaTag.Divide(hEnThetaAll)

    ytit = "Electron energy #it{E} (GeV)"
    xtit = "Electron polar angle #theta (rad)"
    ut.put_yx_tit(hEnThetaTag, ytit, xtit, 1.4, 1.3)

    hEnThetaTag.SetTitleOffset(1.5, "Z")
    hEnThetaTag.SetZTitle("Tagger acceptance")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hEnThetaTag.SetMinimum(0)
    hEnThetaTag.SetMaximum(1)
    hEnThetaTag.SetContour(300)

    hEnThetaTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_theta

#_____________________________________________________________________________
def acc_ly_lx():

    #2D acceptance in Bjorken-x and inelasticity y

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"

    #tagger 1 or 2
    tag = 1

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 0:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

    #bins in log_10(y)
    ybin = 0.04
    ymin = -4
    ymax = 0

    #bins in log_10(x)
    xbin = 0.1
    xmin = -12
    xmax = -1

    can = ut.box_canvas()

    hYXTag = ut.prepare_TH2D("hYXTag", xbin, xmin, xmax, ybin, ymin, ymax)
    hYXAll = ut.prepare_TH2D("hYXAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "TMath::Log10(true_y):TMath::Log10(true_x)" # y:x
    tree.Draw(form+" >> hYXTag", sel)
    tree.Draw(form+" >> hYXAll")

    hYXTag.Divide(hYXAll)

    ytit = "Virtuality #it{y} as log_{10}(#it{y})"
    xtit = "Bjorken-#it{x} as log_{10}(#it{x})"
    ut.put_yx_tit(hYXTag, ytit, xtit, 1.4, 1.3)

    hYXTag.SetTitleOffset(1.5, "Z")
    hYXTag.SetZTitle("Tagger acceptance")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hYXTag.SetMinimum(0)
    hYXTag.SetMaximum(1)
    hYXTag.SetContour(300)

    hYXTag.Draw("colz")

    leg = ut.prepare_leg(0.59, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_ly_lx

#_____________________________________________________________________________
def acc_en_eta():

    #2D acceptance in energy and pseudorapidity

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"

    #bins in eta
    etabin = 0.1
    etamin = -12.9
    etamax = -4.5

    #bins in energy
    ebin = 0.3
    emin = 0
    emax = 20

    #tagger 1 or 2
    tag = 1

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 0:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

    can = ut.box_canvas()

    hEnThetaTag = ut.prepare_TH2D("hEnThetaTag", etabin, etamin, etamax, ebin, emin, emax)
    hEnThetaAll = ut.prepare_TH2D("hEnThetaAll", etabin, etamin, etamax, ebin, emin, emax)

    form = "true_el_E:(-TMath::Log(TMath::Tan(true_el_theta/2.)))"
    tree.Draw(form+" >> hEnThetaTag", sel)
    tree.Draw(form+" >> hEnThetaAll")

    hEnThetaTag.Divide(hEnThetaAll)

    ytit = "Electron energy #it{E} (GeV)"
    xtit = "Electron pseudorapidity #eta"
    ut.put_yx_tit(hEnThetaTag, ytit, xtit, 1.4, 1.3)

    hEnThetaTag.SetTitleOffset(1.5, "Z")
    hEnThetaTag.SetZTitle("Tagger acceptance")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hEnThetaTag.SetMinimum(0)
    hEnThetaTag.SetMaximum(1)
    hEnThetaTag.SetContour(300)

    hEnThetaTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_eta

#_____________________________________________________________________________
def acc_pitheta_s12():

    #acceptance in electron polar angle as  pi - theta  in mrad for tagger 1 and tagger 2

    inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    #mrad
    tmin = 0
    tmax = 12

    amax = 0.3

    as1 = rt.acc_Q2_kine(tree, "true_el_theta", "s1_IsHit")
    as1.modif = 2 # pi - theta, mrad
    as1.prec = 0.05
    as1.bmin = 0.2
    #as1.nev = int(1e5)
    gs1 = as1.get()

    as2 = rt.acc_Q2_kine(tree, "true_el_theta", "s2_IsHit")
    as2.modif = 2 # pi - theta, mrad
    as2.prec = 0.05
    as2.bmin = 0.2
    #as2.nev = int(1e5)
    gs2 = as2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0, tmax, amax)
    ut.put_yx_tit(frame, "Acceptance", "Electron #pi - #it{#theta} (mrad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gs1, rt.kBlue)
    gs1.Draw("psame")

    ut.set_graph(gs2, rt.kRed)
    gs2.Draw("psame")

    gPad.SetGrid()

    #leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry(None, "Tagger 1", "")
    #leg.AddEntry(glQ2Py, "Pythia6", "l")
    #leg.AddEntry(glQ2Qr, "QR", "l")
    #leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_pitheta_s12

#_____________________________________________________________________________
def acc_mlt_theta_s12():

    #acceptance in electron polar angle as  -log10(pi - theta)  in mrad for tagger 1 and tagger 2

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag2a/hits_tag_10files.root"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    #mrad
    tmin = 1.5
    tmax = 7.5

    #amax = 0.3
    amax = 1

    as1 = rt.acc_Q2_kine(tree, "true_el_theta", "s1_IsHit")
    as1.modif = 3 # -log10(pi - theta)
    as1.prec = 0.05
    as1.bmin = 0.1
    #as1.nev = int(1e5)
    gs1 = as1.get()

    as2 = rt.acc_Q2_kine(tree, "true_el_theta", "s2_IsHit")
    as2.modif = 3 # -log10(pi - theta)
    as2.prec = 0.05
    as2.bmin = 0.1
    #as2.nev = int(1e5)
    gs2 = as2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0, tmax, amax)
    ut.put_yx_tit(frame, "Acceptance", "Electron -log_{10}(#pi - #it{#theta}_{e})", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gs1, rt.kBlue)
    gs1.Draw("psame")

    ut.set_graph(gs2, rt.kRed)
    gs2.Draw("psame")

    gPad.SetGrid()

    #leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry(None, "Tagger 1", "")
    #leg.AddEntry(glQ2Py, "Pythia6", "l")
    #leg.AddEntry(glQ2Qr, "QR", "l")
    #leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_mlt_theta_s12

#_____________________________________________________________________________
def acc_en_pitheta():

    #2D acceptance in energy and pi - theta in mrad

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag3a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag3ax1/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag3ax2/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag.root"

    #bins in theta, mrad
    xbin = 0.2
    xmin = 0
    xmax = 12

    #bins in energy, GeV
    ybin = 0.3
    ymin = 1
    ymax = 20

    #tagger 1 or 2
    tag = 0

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 0:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

    can = ut.box_canvas()

    hTag = ut.prepare_TH2D("hTag", xbin, xmin, xmax, ybin, ymin, ymax)
    hAll = ut.prepare_TH2D("hAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "true_el_E:(TMath::Pi()-true_el_theta)*1e3" # mrad
    tree.Draw(form+" >> hTag", sel)
    tree.Draw(form+" >> hAll")

    hTag.Divide(hAll)

    ytit = "Electron energy #it{E} (GeV)"
    xtit = "Electron polar angle #it{#pi}-#it{#theta} (mrad)"
    ut.put_yx_tit(hTag, ytit, xtit, 1.4, 1.3)

    hTag.SetTitleOffset(1.4, "Z")
    hTag.SetZTitle("Tagger acceptance")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hTag.SetMinimum(0)
    hTag.SetMaximum(1)
    hTag.SetContour(300)

    hTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_pitheta

#_____________________________________________________________________________
def acc_lQ2_en():

    #2D acceptance in log_10(Q^2) and energy

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag3a/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag.root"

    #bins in energy, GeV
    xbin = 0.3
    xmin = 1
    xmax = 20

    #bins in log_10(Q^2), GeV^2
    ybin = 0.1
    ymin = -9
    ymax = 0

    #tagger 1 or 2
    tag = 1

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 0:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

    can = ut.box_canvas()

    hTag = ut.prepare_TH2D("hTag", xbin, xmin, xmax, ybin, ymin, ymax)
    hAll = ut.prepare_TH2D("hAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "(TMath::Log10(true_Q2)):true_el_E"
    tree.Draw(form+" >> hTag", sel)
    tree.Draw(form+" >> hAll")

    hTag.Divide(hAll)

    ytit = "Virtuality #it{Q}^{2} (GeV^{2})"
    xtit = "Scattered electron energy #it{E'} (GeV)"
    ut.put_yx_tit(hTag, ytit, xtit, 1.7, 1.3)

    hTag.SetTitleOffset(1.4, "Z")
    hTag.SetZTitle("Tagger acceptance")

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.015, 0.15)

    #labels in power of 10
    ay = hTag.GetYaxis()
    labels = range(ymin, ymax+1, 1)
    for i in range(len(labels)):
        if labels[i] == 0:
            ay.ChangeLabel(i+1, -1, -1, -1, -1, -1, "1")
            continue
        ay.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")
    ay.SetLabelOffset(0.012)

    gPad.SetGrid()

    hTag.SetMinimum(0)
    hTag.SetMaximum(1)
    hTag.SetContour(300)

    hTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_lQ2_en

#_____________________________________________________________________________
def acc_lQ2_pitheta():

    #2D acceptance in log_10(Q^2) and pi - theta in mrad

    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag3a/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag4a/hits_tag.root"

    #bins in theta, mrad
    xbin = 0.3
    xmin = 0
    xmax = 12

    #bins in log_10(Q^2), GeV^2
    ybin = 0.2
    ymin = -9
    ymax = 0

    #tagger 1 or 2
    tag = 1

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    if tag == 0:
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

    can = ut.box_canvas()

    hTag = ut.prepare_TH2D("hTag", xbin, xmin, xmax, ybin, ymin, ymax)
    hAll = ut.prepare_TH2D("hAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "(TMath::Log10(true_Q2)):(TMath::Pi()-true_el_theta)*1e3"
    tree.Draw(form+" >> hTag", sel)
    tree.Draw(form+" >> hAll")

    hTag.Divide(hAll)

    ytit = "Virtuality #it{Q}^{2} (GeV^{2})"
    xtit = "Electron polar angle #it{#pi}-#it{#theta} (mrad)"
    ut.put_yx_tit(hTag, ytit, xtit, 1.7, 1.3)

    hTag.SetTitleOffset(1.4, "Z")
    hTag.SetZTitle("Tagger acceptance")

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.015, 0.15)

    #labels in power of 10
    ay = hTag.GetYaxis()
    labels = range(ymin, ymax+1, 1)
    for i in range(len(labels)):
        if labels[i] == 0:
            ay.ChangeLabel(i+1, -1, -1, -1, -1, -1, "1")
            continue
        ay.ChangeLabel(i+1, -1, -1, -1, -1, -1, "10^{"+str(labels[i])+"}")
    ay.SetLabelOffset(0.012)

    #gPad.SetLogz()

    gPad.SetGrid()

    hTag.SetMinimum(0)
    hTag.SetMaximum(1)
    hTag.SetContour(300)

    hTag.Draw("colz")

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_lQ2_pitheta

#_____________________________________________________________________________
def hit_en():

    #energy in tagger

    #infile = "lmon.root"
    infile = "dd.root"

    emin = 0
    emax = 19
    ebin = 0.1
    #emax = 1.1
    #ebin = 0.01

    inp = TFile.Open(infile)
    tree = inp.Get("event")

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    #nev = tree.Draw("hit_s1_en >> hE", "s1_IsHit==1")
    nev = tree.Draw("hit_s2_en >> hE", "s2_IsHit==1")
    #nev = tree.Draw("hit_s1_en/gen_en >> hE", "s1_IsHit==1")
    #nev = tree.Draw("hit_s2_en/gen_en >> hE", "s2_IsHit==1")
    #nev = tree.Draw("hit_s1_en >> hE", "(s1_IsHit==1)&&((hit_s1_en/gen_en)>0.9)")
    #nev = tree.Draw("hit_s2_en >> hE", "(s2_IsHit==1)&&((hit_s2_en/gen_en)>0.9)")
    print(nev)

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hit_en

#_____________________________________________________________________________
def load_lmon():

    #input
    inp = TFile.Open("../../lmon.root")

    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = -1

    #input generated particles
    pdg = std.vector(int)()
    en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", pdg)
    tree.SetBranchAddress("gen_en", en)

    #input tagger counter hits
    en_s1 = std.vector(float)()
    en_s2 = std.vector(float)()
    tree.SetBranchAddress("lowQ2s1_HitEn", en_s1)
    tree.SetBranchAddress("lowQ2s2_HitEn", en_s2)

    #output
    out = TFile("lmon.root", "recreate")
    otree = TTree("event", "event")
    gen_en = c_double(0)
    hit_s1_en = c_double(0)
    hit_s2_en = c_double(0)
    s1_IsHit = c_bool(0)
    s2_IsHit = c_bool(0)
    otree.Branch("gen_en", gen_en, "gen_en/D")
    otree.Branch("hit_s1_en", hit_s1_en, "hit_s1_en/D")
    otree.Branch("hit_s2_en", hit_s2_en, "hit_s2_en/D")
    otree.Branch("s1_IsHit", s1_IsHit, "s1_IsHit/O")
    otree.Branch("s2_IsHit", s2_IsHit, "s2_IsHit/O")

    #event loop
    if nev<0: nev = tree.GetEntries()
    for ievt in range(nev):
        tree.GetEntry(ievt)

        #generated electron energy
        for imc in range(pdg.size()):
            if pdg.at(imc) == 11: gen_en.value = en.at(imc)

        #tagger hits
        hit_s1_en.value = -1e9
        hit_s2_en.value = -1e9
        s1_IsHit.value = 0
        s2_IsHit.value = 0

        #Tagger 1
        for i in range(en_s1.size()):
            if en_s1.at(i) > hit_s1_en.value: hit_s1_en.value = en_s1.at(i)

        #Tagger 2
        for i in range(en_s2.size()):
            if en_s2.at(i) > hit_s2_en.value: hit_s2_en.value = en_s2.at(i)

        #hit in event
        if hit_s1_en.value > 0: s1_IsHit.value = 1
        if hit_s2_en.value > 0: s2_IsHit.value = 1

        otree.Fill()

    #event loop

    otree.Write()
    out.Close()

#load_lmon

#_____________________________________________________________________________
def load_dd():

    infile = "/home/jaroslav/sim/Athena/athena_particle_counter/output_10k.root"

    store = EventStore([infile])

    #output
    out = TFile("dd.root", "recreate")
    otree = TTree("event", "event")
    gen_en = c_double(0)
    hit_s1_en = c_double(0)
    hit_s2_en = c_double(0)
    s1_IsHit = c_bool(0)
    s2_IsHit = c_bool(0)
    otree.Branch("gen_en", gen_en, "gen_en/D")
    otree.Branch("hit_s1_en", hit_s1_en, "hit_s1_en/D")
    otree.Branch("hit_s2_en", hit_s2_en, "hit_s2_en/D")
    otree.Branch("s1_IsHit", s1_IsHit, "s1_IsHit/O")
    otree.Branch("s2_IsHit", s2_IsHit, "s2_IsHit/O")

    #event loop
    for iev, evt in enumerate(store):

        #print("Next event")

        gen_en.value = -1

        #mc loop
        for imc in store.get("mcparticles"):

            if imc.genStatus() != 1:
                continue

            #generated electron energy
            if imc.pdgID() == 11: gen_en.value = imc.energy()

            #print("mc:", imc.energy(), imc.pdgID(), imc.genStatus(), imc.parents_size())

        #tagger hits
        hit_s1_en.value = -1e9
        hit_s2_en.value = -1e9
        s1_IsHit.value = 0
        s2_IsHit.value = 0

        #Tagger 1
        for ihit in store.get("ParticleCounterS1"):
            #print("hit s1:", ihit.energyDeposit())

            if ihit.energyDeposit()/gen_en.value < 0.9:
                continue

            if ihit.energyDeposit() < hit_s1_en.value:
                continue

            hit_s1_en.value = ihit.energyDeposit()

        #Tagger 2
        for ihit in store.get("ParticleCounterS2"):
            #print("hit s2:", ihit.energyDeposit())

            if ihit.energyDeposit()/gen_en.value < 0.9:
                continue

            if ihit.energyDeposit() < hit_s2_en.value:
                continue

            hit_s2_en.value = ihit.energyDeposit()

        #hit in event
        if hit_s1_en.value > 0: s1_IsHit.value = 1
        if hit_s2_en.value > 0: s2_IsHit.value = 1

        otree.Fill()

    #event loop

    otree.Write()
    out.Close()

#load_dd

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()

















