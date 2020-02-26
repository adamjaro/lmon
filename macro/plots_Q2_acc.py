#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #tagger acceptance as a function of Q2

    iplot = 1
    funclist = []
    funclist.append( acc_quasi_real ) # 0
    funclist.append( acc_pythia ) # 1

    funclist[iplot]()

#main

#_____________________________________________________________________________
def acc_quasi_real():

    #Quasi-real input
    inp_qr = "../data/lmon_18x275_qr_xB_yA_lowQ2_B2eRv2_1Mevt.root"

    #range in the log_10(Q^2)
    lqmin = -4.5
    lqmax = -1.8

    #bins calculation
    prec = 0.02
    delt = 1e-6

    #number of events, 0 for all
    nev = 0

    #tree from the input
    tree_qr, infile_qr = get_tree(inp_qr)

    #calculate the acceptance
    gROOT.LoadMacro("get_acc.C")
    gROOT.LoadMacro("get_Q2_acc.C")

    #electron beam energy and B2eR acceptance
    acc_qr = rt.get_Q2_acc(tree_qr, 18, 0.01021, prec, delt, nev)

    #make the plot
    can = ut.box_canvas()

    ut.set_graph(acc_qr, rt.kRed)

    frame = gPad.DrawFrame(lqmin, 0, lqmax, 0.6)

    frame.Draw()

    acc_qr.Draw("psame")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_quasi_real

#_____________________________________________________________________________
def acc_pythia():

    #Pythia input
    inp_py = "../data/lmon_pythia_5M_1Mevt.root"

    #range in the log_10(Q^2)
    lqmin = -10
    lqmax = 0

    #bins calculation
    prec = 0.04
    delt = 1e-6

    #number of events, 0 for all
    nev = 0

    #tree from the input
    tree_py, infile_py = get_tree(inp_py)

    #calculate the acceptance for both inputs
    gROOT.LoadMacro("get_acc.C")
    gROOT.LoadMacro("get_Q2_acc.C")

    #electron beam energy and B2eR acceptance
    acc_py = rt.get_Q2_acc(tree_py, 18, 0.01021, prec, delt, nev)

    #make the plot
    can = ut.box_canvas()

    ut.set_graph(acc_py, rt.kBlue) # , rt.kFullTriangleUp

    frame = gPad.DrawFrame(lqmin, 0, lqmax, 0.3)

    frame.Draw()

    acc_py.Draw("psame")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_pythia

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

    main()















