#!/usr/bin/python3

from math import tan

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
    inp = TFile.Open("../../data/ew/ew1bx1.root")
    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = -1

    #output
    out = TFile("prim_bx1.root", "recreate")
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

    inp = TFile.Open("ew.root")
    tree = inp.Get("prim_tree")

    can = ut.box_canvas()

    gStyle.SetPalette(55)

    hXY = ut.prepare_TH2D("hXY", xybin, -xymax, xymax, xybin, -xymax, xymax)

    tree.Draw("y:x >> hXY")

    hXY.Draw("colz")

    #circles at a given apperture, radius (mm) = z0*tan(tmax), example: 18644*tan(0.002) = 37 mm
    z0 = 18644. # mm, exit window position in z

    # 2 mrad circle
    tmax = 2. # mrad, apperture by maximal theta for photons
    radius = z0*tan(tmax*1e-3)
    circle = TCrown(0., 0., radius, radius)
    circle.SetLineStyle(2)
    circle.SetLineWidth(4)
    #circle.SetLineColor(rt.kGreen+1)
    circle.SetLineColor(rt.kRed)
    circle.Draw("same")

    #fraction of events at 2 mrad
    nev = tree.GetEntries()
    nrad = float(tree.Draw("", "TMath::Sqrt(x*x+y*y)<"+str(radius)))
    print(nrad, "{0:.2f}".format(100.*nrad/nev))

    # 1 mrad circle
    tmax = 1. # mrad, apperture by maximal theta for photons
    radius = z0*tan(tmax*1e-3)
    circle2 = TCrown(0., 0., radius, radius)
    circle2.SetLineStyle(2)
    circle2.SetLineWidth(4)
    circle2.SetLineColor(rt.kOrange)
    circle2.Draw("same")

    #fraction of events at 1 mrad
    nrad = float(tree.Draw("", "TMath::Sqrt(x*x+y*y)<"+str(radius)))
    print(nrad, "{0:.2f}".format(100.*nrad/nev))

    ut.put_yx_tit(hXY, "#it{y} (mm)", "#it{x} (mm)")

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
    zmax = 300
    zbin = 0.5

    inp = TFile.Open("ew.root")
    tree = inp.Get("prim_tree")

    can = ut.box_canvas()

    hZ = ut.prepare_TH1D("hZ", zbin, -zmax, zmax)

    tree.Draw("z >> hZ")
    ut.line_h1(hZ)

    #lines at 250 mrad projected in z for a given aperture tmax in mrad, example: z (mm) = 18644*tan(0.002)/tan(0.25) = 144.9
    z0 = 18644. # mm, exit window position in z

    #lines for 2 mrad aperture
    tmax = 2. # mrad, apperture by maximal theta for photons
    zlim = z0*tan(tmax*1e-3)/tan(0.25)
    zline = [ut.cut_line(zlim, 0.75, hZ, True), ut.cut_line(-zlim, 0.75, hZ, True)]
    zline[0].SetLineColor(rt.kRed)
    zline[1].SetLineColor(rt.kRed)
    zline[0].Draw("same")
    zline[1].Draw("same")

    #fraction of events at 2 mrad aperture in z, cross check to the xy projection
    nz = float( tree.Draw("", "TMath::Abs(z)<"+str(zlim)) )
    nev = tree.GetEntries()
    print(nz, "{0:.2f}".format(100.*nz/nev))

    #lines at 1 mrad aperture
    tmax = 1. # mrad, apperture by maximal theta for photons
    zlim = z0*tan(tmax*1e-3)/tan(0.25)
    zline2 = [ut.cut_line(zlim, 0.75, hZ, True), ut.cut_line(-zlim, 0.75, hZ, True)]
    zline2[0].SetLineColor(rt.kOrange)
    zline2[1].SetLineColor(rt.kOrange)
    zline2[0].Draw("same")
    zline2[1].Draw("same")

    #fraction of events at 1 mrad aperture in z, cross check to the xy projection
    nz = float( tree.Draw("", "TMath::Abs(z)<"+str(zlim)) )
    print(nz, "{0:.2f}".format(100.*nz/nev))

    ut.put_yx_tit(hZ, "Counts", "#it{z} (mm)")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.03)

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#z_proj

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











