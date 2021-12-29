#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = mlt

    func[iplot]()

#_____________________________________________________________________________
def mlt():

    # mlt = -log_10(pi-true_el_theta)

    #input
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1a/hits_tag.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag1ax1/hits_tag.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag2a/hits_tag_10files.root"

    #condition
    cond = ""
    #cond += "(s1_IsHit==1)"
    cond += "(s2_IsHit==1)&&(true_el_E>0)&&(true_el_E<18)"
    #cond += "(s1_IsHit==1)||(s2_IsHit==1)"

    infile = TFile.Open(inp)
    tree = infile.Get("event")

    #mlt range
    #tbin = 0.1
    #tmin = -2
    #tmax = 8
    tbin = 0.1
    tmin = 0
    tmax = 12

    hT = ut.prepare_TH1D("hT", tbin, tmin, tmax)

    can = ut.box_canvas()

    #form = "-TMath::Log10(TMath::Pi()-true_el_theta)"
    form = "(TMath::Pi()-true_el_theta)*1e3"
    tree.Draw(form+" >> hT", cond)

    ut.put_yx_tit(hT, "Events", "mlt", 1.4, 1.2)

    hT.Draw()

    gPad.SetLogy()
    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#mlt

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()










