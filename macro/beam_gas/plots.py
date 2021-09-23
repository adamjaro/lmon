#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = zpos
    func[1] = rpos

    func[iplot]()

#main

#_____________________________________________________________________________
def zpos():

    #hit position in z and vertex position in z

    zmin = -5.5
    zmax = 15.5
    zbin = 0.2

    infile = TFile.Open("rc.root")
    tree = infile.Get("rtree")

    can = ut.box_canvas()

    hz = ut.prepare_TH2D("hz", zbin, zmin, zmax, zbin, -zmax, zmax)

    tree.Draw("(zpos/1e3):(vtx_z/1e3) >> hz")

    print("Entries:", hz.GetEntries())

    hz.SetXTitle("Vertex #it{z} (m)")
    hz.SetYTitle("Hit #it{z} (m)")

    hz.SetTitleOffset(1.3, "Y")
    hz.SetTitleOffset(1.3, "X")

    hz.GetXaxis().CenterTitle()
    hz.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hz.SetMinimum(0.98)
    hz.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#zpos

#_____________________________________________________________________________
def rpos():

    #radial hit position and vertex position in z

    #meters
    zmin = -5.5
    zmax = 17
    zbin = 0.2

    #cm
    rmin = 3.2
    rmax = 14
    rbin = 0.1

    infile = TFile.Open("rc_z0.root")
    tree = infile.Get("rtree")

    can = ut.box_canvas()

    hz = ut.prepare_TH2D("hz", zbin, zmin, zmax, rbin, rmin, rmax)

    tree.Draw("(rpos/1e1):(vtx_z/1e3) >> hz")

    print("Entries:", hz.GetEntries())

    hz.SetXTitle("Vertex #it{z} (m)")
    hz.SetYTitle("Hit #it{r} (cm)")

    hz.SetTitleOffset(1.3, "Y")
    hz.SetTitleOffset(1.3, "X")

    hz.GetXaxis().CenterTitle()
    hz.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hz.SetMinimum(0.98)
    hz.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rpos

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()







