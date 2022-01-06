#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2

    func = {}
    func[0] = lQ2
    func[1] = pitheta
    func[2] = energy
    func[3] = eta

    func[iplot]()

#main

#_____________________________________________________________________________
def lQ2():

    #acceptance in log_10(Q^2)

    i1 = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    i2 = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    #tag = ["s1_IsHit", "Tagger 1", 0.15]
    tag = ["s2_IsHit", "Tagger 2", 0.25]

    in1 = TFile.Open(i1)
    t1 = in1.Get("event")
    in2 = TFile.Open(i2)
    t2 = in2.Get("event")

    lQ2min = -9
    lQ2max = 0

    #amax = 0.21
    #amax = 0.25

    a1 = rt.acc_Q2_kine(t1, "true_Q2", tag[0])
    a1.modif = 1 # log_10(Q^2) from Q2
    a1.prec = 0.05
    a1.bmin = 0.1
    #a1.nev = int(1e5)
    g1 = a1.get()

    a2 = rt.acc_Q2_kine(t2, "true_Q2", tag[0])
    a2.modif = 1 # log_10(Q^2) from Q2
    a2.prec = 0.05
    a2.bmin = 0.1
    #a2.nev = int(1e5)
    g2 = a2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(lQ2min, 0, lQ2max, tag[2])
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

    ut.set_graph(g1, rt.kRed)
    g1.Draw("psame")

    ut.set_graph(g2, rt.kBlue)
    g2.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.8, 0.24, 0.14, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", tag[1], "")
    leg.AddEntry(g1, "Quasi-real photoproduction", "lp")
    leg.AddEntry(g2, "Pythia 6", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#lQ2

#_____________________________________________________________________________
def pitheta():

    #acceptance in electron polar angle as  pi - theta  in mrad

    i1 = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    i2 = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    #tag = ["s1_IsHit", "Tagger 1", 0.2]
    tag = ["s2_IsHit", "Tagger 2", 0.3]

    in1 = TFile.Open(i1)
    t1 = in1.Get("event")
    in2 = TFile.Open(i2)
    t2 = in2.Get("event")

    #mrad
    xmin = 0
    xmax = 12

    a1 = rt.acc_Q2_kine(t1, "true_el_theta", tag[0])
    a1.modif = 2 # pi - theta, mrad
    a1.prec = 0.05
    a1.bmin = 0.2
    #a1.nev = int(1e5)
    g1 = a1.get()

    a2 = rt.acc_Q2_kine(t2, "true_el_theta", tag[0])
    a2.modif = 2 # pi - theta, mrad
    a2.prec = 0.05
    a2.bmin = 0.2
    #a2.nev = int(1e5)
    g2 = a2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(xmin, 0, xmax, tag[2])
    ut.put_yx_tit(frame, "Tagger acceptance", "Electron polar angle #it{#pi}-#it{#theta} (mrad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(g1, rt.kRed)
    g1.Draw("psame")

    ut.set_graph(g2, rt.kBlue)
    g2.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.8, 0.24, 0.14, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", tag[1], "")
    leg.AddEntry(g1, "Quasi-real photoproduction", "lp")
    leg.AddEntry(g2, "Pythia 6", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pitheta

#_____________________________________________________________________________
def energy():

    #acceptance in electron energy

    i1 = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    i2 = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    #tag = ["s1_IsHit", "Tagger 1", 2]
    tag = ["s2_IsHit", "Tagger 2", 11]

    in1 = TFile.Open(i1)
    t1 = in1.Get("event")
    in2 = TFile.Open(i2)
    t2 = in2.Get("event")

    #mrad
    xmin = tag[2]
    xmax = 19

    amax = 0.9

    a1 = rt.acc_Q2_kine(t1, "true_el_E", tag[0])
    a1.prec = 0.05
    a1.bmin = 0.1
    #a1.nev = int(1e5)
    g1 = a1.get()

    a2 = rt.acc_Q2_kine(t2, "true_el_E", tag[0])
    a2.prec = 0.05
    a2.bmin = 0.1
    #a2.nev = int(1e5)
    g2 = a2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(xmin, 0, xmax, amax)
    ut.put_yx_tit(frame, "Tagger acceptance", "Electron energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(g1, rt.kRed)
    g1.Draw("psame")

    ut.set_graph(g2, rt.kBlue)
    g2.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.8, 0.24, 0.14, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", tag[1], "")
    leg.AddEntry(g1, "Quasi-real photoproduction", "lp")
    leg.AddEntry(g2, "Pythia 6", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#energy

#_____________________________________________________________________________
def eta():

    #acceptance in electron polar angle as  pi - theta  in mrad

    i1 = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    i2 = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"

    #tag = ["s1_IsHit", "Tagger 1", 0.15]
    tag = ["s2_IsHit", "Tagger 2", 0.3]

    in1 = TFile.Open(i1)
    t1 = in1.Get("event")
    in2 = TFile.Open(i2)
    t2 = in2.Get("event")

    #eta
    xmin = -17
    xmax = -3

    a1 = rt.acc_Q2_kine(t1, "true_el_theta", tag[0])
    a1.modif = 0 # eta from theta
    a1.prec = 0.01
    a1.bmin = 0.1
    #a1.nev = int(1e5)
    g1 = a1.get()

    a2 = rt.acc_Q2_kine(t2, "true_el_theta", tag[0])
    a2.modif = 0 # eta from theta
    a2.prec = 0.01
    a2.bmin = 0.1
    #a2.nev = int(1e5)
    g2 = a2.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(xmin, 0, xmax, tag[2])
    ut.put_yx_tit(frame, "Tagger acceptance", "Electron pseudorapidity #it{#eta}", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(g1, rt.kRed)
    g1.Draw("psame")

    ut.set_graph(g2, rt.kBlue)
    g2.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.8, 0.24, 0.14, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", tag[1], "")
    leg.AddEntry(g1, "Quasi-real photoproduction", "lp")
    leg.AddEntry(g2, "Pythia 6", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#eta

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()























