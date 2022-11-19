#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = xy
    func[1] = theta_x
    func[2] = theta_y
    func[3] = dx
    func[4] = d_theta_x
    func[5] = d_theta_y

    func[iplot]()

#main

#_____________________________________________________________________________
def xy():

    #reference position in xy

    #mm
    xybin = 1
    xymax = 100

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v4.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v9.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v5.root"

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
    #xybin = 1
    xybin = 0.1
    #xymax = 100
    #xymax = 10
    xymax = 3

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v9.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v4.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("(1e3*theta_x):(1e3*ref_theta_x) >> hxy", "(is_associate==1)&&(is_prim==1)")
    #tree.Draw("(1e3*theta_x):(1e3*ref_theta_x) >> hxy", "is_prim==1")

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

    leg = ut.prepare_leg(0.15, 0.85, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
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
    #xybin = 1
    xybin = 0.1
    #xymax = 30
    #xymax = 100
    xymax = 8

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v9.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v4.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", xybin, -xymax, xymax, xybin, -xymax, xymax)

    #tree.Draw("(1e3*theta_y):(1e3*ref_theta_y) >> hxy", "is_associate==1")
    tree.Draw("(1e3*theta_y):(1e3*ref_theta_y) >> hxy", "is_prim==1")

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
def dx():

    #track x  -  ref x

    #mm
    xbin = 1e-3
    xmax = 0.14

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v4.root"

    det = "s1_tracks"
    #det = "s2_tracks"

    val = "pos_x-ref_x"
    #val = "pos_y-ref_y"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hx = ut.prepare_TH1D("hx", xbin, -xmax, xmax)

    tree.Draw(val+" >> hx", "is_associate==1")

    ut.put_yx_tit(hx, "Counts", "Track #it{x_{0}}-#it{x_{0,ref}} (mm)", 1.4, 1.3)

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    #gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#dx

#_____________________________________________________________________________
def d_theta_x():

    #track x  -  ref x

    #mm
    xbin = 1e-3
    xmax = 0.2
    #xbin = 1
    #xmax = 200

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v4.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hx = ut.prepare_TH1D("hx", xbin, -xmax, xmax)

    tree.Draw("(1e3*theta_x)-(1e3*ref_theta_x) >> hx", "is_associate==1")

    ut.put_yx_tit(hx, "Counts", "Track #it{#theta}_{x}-#it{#theta}_{x,ref} (mrad)", 1.4, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.02, 0.03)

    gPad.SetLogy()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.87, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#d_theta_x

#_____________________________________________________________________________
def d_theta_y():

    #track y  -  ref y

    #mm
    xbin = 1e-3
    xmax = 0.2
    #xbin = 1
    #xmax = 200

    #inp = "/home/jaroslav/sim/lmon/analysis_tasks/ini/ana.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v4.root"

    #det = "s1_tracks"
    det = "s2_tracks"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hx = ut.prepare_TH1D("hx", xbin, -xmax, xmax)

    tree.Draw("(1e3*theta_y)-(1e3*ref_theta_y) >> hx", "is_associate==1")

    ut.put_yx_tit(hx, "Counts", "Track #it{#theta}_{y}-#it{#theta}_{y,ref} (mrad)", 1.4, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.02, 0.03)

    gPad.SetLogy()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.87, 0.24, 0.1, 0.04) # x, y, dx, dy, tsiz
    tnam = {"s1_tracks": "Tagger 1", "s2_tracks": "Tagger 2"}
    leg.AddEntry("", "#bf{"+tnam[det]+"}", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#d_theta_y

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()



















