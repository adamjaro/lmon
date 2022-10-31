#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2

    func = {}
    func[0] = xy
    func[1] = theta_x
    func[2] = theta_y

    func[iplot]()

#main

#_____________________________________________________________________________
def xy():

    #reference position in xy

    #mm
    xybin = 1
    xymax = 80

    inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v4.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v5.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    #val = "pos_x:ref_x"
    val = "pos_y:ref_y"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw(val+" >> hxy", "is_associate==1")

    hxy.SetXTitle("Reference #it{x_{0}} (mm)")
    hxy.SetYTitle("Track #it{x_{0}} (mm)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    hxy.GetXaxis().CenterTitle()
    hxy.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#xy

#_____________________________________________________________________________
def theta_x():

    #reference angle along x

    #mrad
    xybin = 1
    xymax = 100

    inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v4.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic.root"

    det = "s1_tracks"
    #det = "s2_tracks"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("(1e3*theta_x):(1e3*ref_theta_x) >> hxy", "is_associate==1")

    hxy.SetXTitle("Reference #it{#theta_{x}} (mrad)")
    hxy.SetYTitle("Track #it{#theta_{x}} (mrad)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    hxy.GetXaxis().CenterTitle()
    hxy.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#theta_x

#_____________________________________________________________________________
def theta_y():

    #reference angle along y

    #mrad
    xybin = 1
    #xymax = 50
    xymax = 100

    inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v4.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("(1e3*theta_y):(1e3*ref_theta_y) >> hxy", "is_associate==1")

    hxy.SetXTitle("Reference #it{#theta_{y}} (mrad)")
    hxy.SetYTitle("Track #it{#theta_{y}} (mrad)")

    hxy.SetTitleOffset(1.3, "Y")
    hxy.SetTitleOffset(1.3, "X")

    hxy.GetXaxis().CenterTitle()
    hxy.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#theta_y

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()



















