#!/usr/bin/python3

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem
from ROOT import addressof, TTree, TCrown

from ew_hits import ew_hits

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2
    funclist = []
    funclist.append( make_prim_tree ) # 0
    funclist.append( xy_proj ) # 1
    funclist.append( z_proj ) # 2

    funclist[iplot]()

#main

#_____________________________________________________________________________
def make_prim_tree():

    #input
    #inp = TFile.Open("../../lmon.root")
    inp = TFile.Open("../../data/ew/ew1b.root")
    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = -1

    #output
    out = TFile("prim.root", "recreate")
    gROOT.ProcessLine( "struct EntryF {Float_t v;};" )
    x = rt.EntryF()
    y = rt.EntryF()
    z = rt.EntryF()
    en = rt.EntryF()
    otree = TTree("prim_tree", "prim_tree")
    otree.Branch("x", addressof(x, "v"), "x/F")
    otree.Branch("y", addressof(y, "v"), "y/F")
    otree.Branch("z", addressof(z, "v"), "z/F")
    otree.Branch("en", addressof(en, "v"), "en/F")

    hits = ew_hits("ew", tree)

    if nev<0: nev = tree.GetEntries()
    for ievt in range(nev):
        tree.GetEntry(ievt)

        #print("Next event")

        for ihit in range(hits.get_n()):

            hit = hits.get_hit(ihit)

            #hit by primary photon
            if hit.prim == 0 or hit.pdg != 22: continue

            hit.global_to_zpos(-18644) # mm

            x.v = hit.x
            y.v = hit.y
            z.v = hit.z
            z.en = hit.en

            otree.Fill()

            #print(hit.x, hit.y, hit.z) # , hit.en
            #print(hit.pdg, hit.prim, hit.conv)

            #only first hit by primary particle
            break

    otree.Write()
    out.Close()

#make_prim_tree

#_____________________________________________________________________________
def xy_proj():

    #xy projection for primary photons

    #plot range, upper and lower, mm
    xymax = 50
    xybin = 0.5

    inp = TFile.Open("prim.root")
    tree = inp.Get("prim_tree")

    can = ut.box_canvas()

    #gStyle.SetPalette(56)

    hXY = ut.prepare_TH2D("hXY", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("y:x >> hXY")

    hXY.Draw("colz")

    #circle at two mrad, radius (mm) = 18644*tan(0.002) = 37 mm
    circle = TCrown(0., 0., 37, 37)
    circle.SetLineStyle(2)
    circle.SetLineWidth(4)
    circle.SetLineColor(rt.kRed)
    circle.Draw("same")

    hXY.SetXTitle("#it{x} (mm)")
    hXY.SetYTitle("#it{y} (mm)")

    hXY.SetTitleOffset(1.6, "Y")
    hXY.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.12, 0.02, 0.11)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#xy_proj

#_____________________________________________________________________________
def z_proj():

    #z projection for primary photons

    #plot range, upper and lower, mm
    zmax = 200
    zbin = 0.5

    inp = TFile.Open("prim.root")
    tree = inp.Get("prim_tree")

    can = ut.box_canvas()

    hZ = ut.prepare_TH1D("hZ", zbin, -zmax, zmax)

    tree.Draw("z >> hZ")
    ut.line_h1(hZ)

    #lines at 250 mrad projected in z, z (mm) = 37./tan(0.25) = 144.9
    zhigh = ut.cut_line(144.9, 0.5, hZ, True)
    zhigh.Draw("same")
    zlow = ut.cut_line(-144.9, 0.5, hZ, True)
    zlow.Draw("same")

    ut.put_yx_tit(hZ, "Counts", "#it{z} (mm)")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.01)

    gPad.SetGrid()

    gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#z_proj

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











