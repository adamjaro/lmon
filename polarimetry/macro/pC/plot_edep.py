#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append("/home/jaroslav/sim/lmon/macro")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    #input
    inp = TFile.Open("events.root")
    tree = inp.Get("event")

    #layer to plot
    plot = "lay11_edep"

    #MeV
    ebin = 0.1
    ekmax = 20.
    edmax = 6
    hE = ut.prepare_TH2D("hE", ebin, 0, ekmax, ebin, 0, edmax)

    can = ut.box_canvas()
    tree.Draw(plot+":ekin >> hE", plot+">0.")

    hE.SetXTitle("#it{E}_{kin} (MeV)")
    hE.SetYTitle("#it{E}_{dep} (MeV)")

    hE.SetTitleOffset(1.3, "Y")
    hE.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hE.SetMinimum(0.98)
    hE.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()


