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
    func[2] = en_r_z

    func[iplot]()

#main

#_____________________________________________________________________________
def zpos():

    #hit position in z and vertex position in z

    zmin = -5.5
    zmax = 15.5
    zbin = 0.2

    infile = TFile.Open("rc_ecal.root")
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
    #zmin = 2
    zmin = -6
    zmax = 16
    zbin = 1

    #cm
    #rmin = 3.2
    #rmax = 17
    #rbin = 1
    rmin = 3
    rmax = 4.5
    rbin = 1e-2

    #infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_1a.root"
    infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_2f.root"

    infile = TFile.Open(infile)
    tree = infile.Get("ptree")

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

    for ix in range(1, hz.GetNbinsX()+1):
        for iy in range(1, hz.GetNbinsY()+1):

            pass
            #print(ix, iy, hz.GetBinContent(ix, iy))

    #hz.Draw("colztext")

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rpos

#_____________________________________________________________________________
def en_r_z():

    #radial hit position and vertex position in z

    #meters
    zmin = 2
    zmax = 16
    zbin = 0.2

    #cm
    rmin = 3.2
    rmax = 15
    rbin = 0.2

    #GeV
    emin = 0.1
    emax = 10
    ebin = 0.1

    infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_1a.root"

    infile = TFile.Open(infile)
    tree = infile.Get("ptree")

    can = ut.box_canvas()

    hz = ut.prepare_TH3D("hz", zbin, zmin, zmax, rbin, rmin, rmax, ebin, emin, emax)

    tree.Draw("en:(rpos/1e1):(vtx_z/1e3) >> hz")

    profile = hz.Project3DProfile("yx")

    #print("Entries:", profile.GetEntries())

    profile.SetXTitle("Vertex #it{z} position (m)")
    profile.SetYTitle("Radius #it{r_{xy}} (cm) at #it{z} = 0")
    profile.SetZTitle("Photon energy (GeV)")
    profile.SetTitle("")

    profile.SetTitleOffset(1.3, "X")
    profile.SetTitleOffset(1.3, "Z")

    profile.GetXaxis().CenterTitle()
    profile.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.03, 0.15)

    profile.SetContour(300)

    #gPad.SetLogz()

    profile.Draw("colz")

    leg = ut.prepare_leg(0.2, 0.88, 0.18, 0.08, 0.035)
    leg.AddEntry("", "Plane at #it{z} = 0", "")
    leg.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_r_z

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()







