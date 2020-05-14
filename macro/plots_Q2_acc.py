#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #tagger acceptance as a function of Q2

    iplot = 3
    funclist = []
    funclist.append( acc_quasi_real ) # 0
    funclist.append( acc_pythia ) # 1
    funclist.append( acc_both ) # 2
    funclist.append( acc_gap_both ) # 3

    funclist[iplot]()

#main

#_____________________________________________________________________________
def acc_quasi_real(do_plot=True):

    #Quasi-real input
    inp_qr = "../data/test/lmon.root"
    #inp_qr = "../data/lmon_18x275_qr_xB_yA_lowQ2_B2eRv2_1Mevt.root"
    #inp_qr = "../data/lmon_18x275_qr_xD_yC_1Mevt.root"
    #inp_qr = "../data/lmon_18x275_qr_Qb_1Mevt.root"
    #inp_qr = "../data/lmon_18x275_qr_Qc_10Mevt.root"
    #inp_qr = "../data/lmon_18x275_qr_Qb_beff2_1Mevt.root"

    #range in the log_10(Q^2)
    #lqmin = -4.5
    lqmin = -10
    lqmax = 2 # 0

    #bins calculation
    prec = 0.05
    delt = 1e-6

    #number of events, 0 for all
    #nev = 100000
    nev = 0

    #tree from the input
    tree_qr, infile_qr = get_tree(inp_qr)

    #calculate the acceptance
    #gROOT.LoadMacro("get_acc.C")
    #gROOT.LoadMacro("get_Q2_acc.C")

    #electron beam energy and B2eR acceptance
    acc_qr = rt.get_Q2_acc(tree_qr, 18, 0.01021, prec, delt, nev)

    if do_plot is False:
        return acc_qr

    #make the plot
    can = ut.box_canvas()

    ut.set_graph(acc_qr, rt.kRed) # , rt.kRed

    frame = gPad.DrawFrame(lqmin, 0, lqmax, 1.1) # 0.25

    ytit = "Acceptance / {0:.1f} %".format(prec*100)
    ut.put_yx_tit(frame, ytit, "log_{10}(#it{Q}^{2})", 1.6, 1.2)
    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()

    acc_qr.Draw("psame")

    leg = ut.prepare_leg(0.2, 0.84, 0.2, 0.1, 0.035)
    leg.AddEntry(acc_qr, "Acceptance for quasi-real photoproduction", "lp")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_quasi_real

#_____________________________________________________________________________
def acc_pythia(do_plot=True, sel_mode=1):

    #selection mode, 1 - s1,  2 - s2,  3 - s1 or s2,  4 - ecal,  5 - any

    #Pythia input
    #inp_py = "../data/lmon_pythia_5M_1Mevt.root"
    #inp_py = "../data/lmon_pythia_5M_beff2_1Mevt.root"
    #inp_py = "../data/lmon_pythia_5M_beff2_5Mevt.root"
    inp_py = "../data/ir6/lmon_pythia_5M_beff2_5Mevt.root"
    #inp_py = "../data/ir6_close/lmon_pythia_5M_beff2_close_5Mevt.root"

    #range in the log_10(Q^2)
    lqmin = -10
    lqmax = 5

    #bins calculation
    prec = 0.02 # 0.02  0.06
    delt = 1e-6

    #number of events, 0 for all
    #nev = 200000
    nev = 0

    #tree from the input
    tree_py, infile_py = get_tree(inp_py)

    #calculate the acceptance
    acalc = rt.acc_Q2_calc(tree_py, 18, prec, delt, nev)

    acalc.sel_mode = sel_mode

    #acalc.lQ2min = -2.4
    #acalc.lQ2max = -0.5

    acc_py = acalc.get_acc()

    acalc.release_tree()

    #return

    #electron beam energy and B2eR acceptance
    #acc_py = rt.get_Q2_acc(tree_py, 18, 0.01021, prec, delt, nev)

    if do_plot is False:
        return acc_py

    #make the plot
    can = ut.box_canvas()

    #ut.set_graph(acc_py, rt.kRed) # , rt.kFullTriangleUp
    ut.set_graph(acc_py, rt.kBlack)

    frame = gPad.DrawFrame(lqmin, 0, lqmax, 0.4)

    ytit = "Acceptance / {0:.1f} %".format(prec*100)
    ut.put_yx_tit(frame, ytit, "log_{10}(#it{Q}^{2})", 1.6, 1.2)
    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()

    acc_py.Draw("psame")

    leg = ut.prepare_leg(0.2, 0.84, 0.2, 0.1, 0.035)
    leg.AddEntry(acc_py, "Acceptance for Pythia6", "lp")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_pythia

#_____________________________________________________________________________
def acc_gap(inp, lqmin = -2.4, lqmax = -0.5):

    #acceptance in selected gap region

    #bins calculation
    prec = 0.02 # 0.02  0.06
    delt = 1e-6

    #number of events, 0 for all
    #nev = 200000
    nev = 0

    #tree from the input
    tree_py, infile_py = get_tree(inp)

    #calculate the acceptance
    acalc = rt.acc_Q2_calc(tree_py, 18, prec, delt, nev)

    acalc.sel_mode = 5

    #range in the log_10(Q^2) for acceptance calculation
    acalc.lQ2min = lqmin
    acalc.lQ2max = lqmax

    acc_py = acalc.get_acc()

    return acc_py

#acc_gap

#_____________________________________________________________________________
def acc_both():

    #acceptance for quasi-real photoproduction and for Pythia

    #selection mode, 1 - s1,  2 - s2,  3 - s1 or s2,  4 - ecal,  5 - any

    #acc_qr = acc_quasi_real(False)
    acc_py_s1 = acc_pythia(False, 1)
    acc_py_s2 = acc_pythia(False, 2)
    #acc_py_s12 = acc_pythia(False, 3)
    acc_py_ecal = acc_pythia(False, 4)
    acc_py_all = acc_pythia(False, 5)

    #acc_py = acc_gap("../data/ir6_close/lmon_pythia_5M_beff2_close_5Mevt.root")

    #make the plot
    can = ut.box_canvas()

    #ut.set_graph(acc_qr, rt.kRed)
    #ut.set_graph(acc_py, rt.kBlue, rt.kFullTriangleUp)

    ut.set_graph(acc_py_s1, rt.kYellow+1)
    ut.set_graph(acc_py_s2, rt.kGreen+1)
    #ut.set_graph(acc_py_s12, rt.kBlack)
    ut.set_graph(acc_py_ecal, rt.kBlue)
    ut.set_graph(acc_py_all, rt.kBlack)

    frame = gPad.DrawFrame(-10, 0, 5, 1.1) # 0.3
    frame.Draw()

    #ytit = "Acceptance / {0:.1f} %".format(prec*100)
    ut.put_yx_tit(frame, "Acceptance", "log_{10}(#it{Q}^{2})", 1.6, 1.2)
    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()

    #acc_py.Draw("psame")
    #acc_qr.Draw("psame")

    acc_py_s1.Draw("psame")
    acc_py_s2.Draw("psame")
    #acc_py_s12.Draw("psame")
    acc_py_all.Draw("psame")
    acc_py_ecal.Draw("psame")

    #leg = ut.prepare_leg(0.2, 0.82, 0.2, 0.12, 0.035)
    leg = ut.prepare_leg(0.15, 0.78, 0.2, 0.16, 0.035)
    #leg.AddEntry(acc_qr, "Quasi-real photoproduction", "lp")
    #leg.AddEntry(acc_py, "Pythia6", "lp")
    leg.AddEntry(acc_py_s1, "Tagger 1", "lp")
    leg.AddEntry(acc_py_s2, "Tagger 2", "lp")
    #leg.AddEntry(acc_py_s12, "Tagger 1 #bf{or} Tagger 2", "lp")
    leg.AddEntry(acc_py_ecal, "ecal", "lp")
    leg.AddEntry(acc_py_all, "Tagger 1 #bf{or} Tagger 2 #bf{or} ecal", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_both

#_____________________________________________________________________________
def acc_gap_both():

    #acceptance in gap between taggers and ecal

    acc_py = acc_gap("../data/ir6/lmon_pythia_5M_beff2_5Mevt.root")
    acc_py_close = acc_gap("../data/ir6_close/lmon_pythia_5M_beff2_close_5Mevt.root", -2.4, 0)

    #make the plot
    can = ut.box_canvas()

    ut.set_graph(acc_py, rt.kBlue)
    ut.set_graph(acc_py_close, rt.kRed)

    frame = gPad.DrawFrame(-3, 0, 0.1, 1.1)
    frame.Draw()

    #ytit = "Acceptance / {0:.1f} %".format(prec*100)
    ut.put_yx_tit(frame, "Acceptance", "log_{10}(#it{Q}^{2})", 1.6, 1.2)
    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()

    acc_py.Draw("psame")
    acc_py_close.Draw("psame")

    leg = ut.prepare_leg(0.2, 0.84, 0.2, 0.1, 0.035)
    #leg.AddEntry(acc_qr, "Quasi-real photoproduction", "lp")
    #leg.AddEntry(acc_py, "Pythia6", "lp")
    leg.AddEntry(acc_py, "Default geometry", "lp")
    leg.AddEntry(acc_py_close, "Magnets in central det", "lp")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_gap_both

#_____________________________________________________________________________
def get_tree(infile):

    #get tree from input file

    inp = TFile.Open(infile)
    return inp.Get("DetectorTree"), inp

#get_tree

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    #for acceptance calculation
    #gROOT.LoadMacro("get_acc.C")
    #gROOT.LoadMacro("get_Q2_acc.C")
    #gROOT.LoadMacro("acc_Q2_calc.C")

    gROOT.ProcessLine(".include .")
    gROOT.ProcessLine(".L acc_Q2_calc.C+")

    main()















