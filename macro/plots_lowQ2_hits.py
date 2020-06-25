#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile

import plot_utils as ut
from BoxCalV2Hits import BoxCalV2Hits

#_____________________________________________________________________________
def main():

    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_1Mevt.root"
    infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_NoFilter_1Mevt.root"

    iplot = 4
    funclist = []
    funclist.append( hits_xy_s1 ) # 0
    funclist.append( hits_xy_s2 ) # 1
    funclist.append( hits_en_z_s1 ) # 2
    funclist.append( hits_en_z_s2 ) # 3
    funclist.append( hits_en ) # 4

    #input
    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("DetectorTree")

    #call the plot function
    funclist[iplot]()

#main

#_____________________________________________________________________________
def hits_xy_s1():

    #hits on s1 tagger in xy

    xybin = 0.3
    xpos = 51
    xysiz = 42

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, xpos-(xysiz/2.), xpos+(xysiz/2.), xybin, -xysiz/2., xysiz/2.)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("lowQ2s1", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hXY.Fill(hits.GetX(ihit)/10, hits.GetY(ihit)/10)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_xy_s1

#_____________________________________________________________________________
def hits_xy_s2():

    #hits on s2 tagger in xy

    xybin = 0.1
    xpos = 63
    xysiz = 28

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, xpos-(xysiz/2.), xpos+(xysiz/2.), xybin, -xysiz/2., xysiz/2.)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("lowQ2s2", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hXY.Fill(hits.GetX(ihit)/10, hits.GetY(ihit)/10)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_xy_s2

#_____________________________________________________________________________
def hits_en_z_s1():

    #energy along the z position of the hit in s1

    zpos = -24000 # mm
    zbin = 0.1 # cm
    zmax = 2 # cm
    zmin = -36 # cm

    ebin = 0.1
    emin = 0
    emax = 20

    can = ut.box_canvas()
    hEnZ = ut.prepare_TH2D("hEnZ", zbin, zmin, zmax, ebin, emin, emax)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("lowQ2s1", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hEnZ.Fill( (hits.GetZ(ihit)-zpos)/10, hits.GetEn(ihit))

    hEnZ.SetMinimum(0.98)
    hEnZ.SetContour(300)

    hEnZ.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_en_z_s1

#_____________________________________________________________________________
def hits_en_z_s2():

    #energy along the z position of the hit in s2

    zpos = -37000 # mm
    zbin = 0.1 # cm
    zmax = 2 # cm
    zmin = -36 # cm

    ebin = 0.1
    emin = 0
    emax = 20

    can = ut.box_canvas()
    hEnZ = ut.prepare_TH2D("hEnZ", zbin, zmin, zmax, ebin, emin, emax)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("lowQ2s2", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hEnZ.Fill( (hits.GetZ(ihit)-zpos)/10, hits.GetEn(ihit))

    hEnZ.SetMinimum(0.98)
    hEnZ.SetContour(300)

    hEnZ.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_en_z_s2

#_____________________________________________________________________________
def hits_en():

    #energy of the hits

    ebin = 0.1
    emin = 0
    emax = 20

    name = "lowQ2s1"

    can = ut.box_canvas()
    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits(name, tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        en_evt = 0.

        for ihit in xrange(hits.GetN()):
            en_evt += hits.GetEn(ihit)

        hE.Fill( en_evt )

    hE.Draw()

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_en


#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()




















