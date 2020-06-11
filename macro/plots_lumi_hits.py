#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile

import plot_utils as ut
from BoxCalV2Hits import BoxCalV2Hits

#_____________________________________________________________________________
def main():

    infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_1Mevt.root"
    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_NoFilter_1Mevt.root"

    iplot = 5
    funclist = []
    funclist.append( hits_xy_phot ) # 0
    funclist.append( hits_xy_up ) # 1
    funclist.append( hits_xy_down ) # 2
    funclist.append( hits_en_z_phot ) # 3
    funclist.append( hits_en_z_up ) # 4
    funclist.append( hits_en_z_down ) # 5

    #input
    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("DetectorTree")

    #call the plot function
    funclist[iplot]()

#main

#_____________________________________________________________________________
def hits_xy_phot():

    #hits on photon detector in xy

    xybin = 0.1
    xysiz = 22

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xysiz/2., xysiz/2., xybin, -xysiz/2., xysiz/2.)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("phot", tree)
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

#hits_xy_phot

#_____________________________________________________________________________
def hits_xy_up():

    #hits on up spectrometer detector in xy

    ypos = 14.2 # cm
    xybin = 0.1 # cm
    xysiz = 22 # cm

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xysiz/2., xysiz/2., xybin, ypos-(xysiz/2.), ypos+(xysiz/2.))

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("up", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hXY.Fill(hits.GetX(ihit)/10, hits.GetY(ihit)/10)

            #print hits.GetX(ihit)/10, hits.GetY(ihit)/10

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_xy_up

#_____________________________________________________________________________
def hits_xy_down():

    #hits on down spectrometer detector in xy

    ypos = -14.2 # cm
    xybin = 0.1 # cm
    xysiz = 22 # cm

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xysiz/2., xysiz/2., xybin, ypos-(xysiz/2.), ypos+(xysiz/2.))

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("down", tree)
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

#hits_xy_down

#_____________________________________________________________________________
def hits_en_z_phot():

    #energy along the z position of the hit in photon detector

    zpos = -37774 # mm
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

    hits = BoxCalV2Hits("phot", tree)
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

#hits_en_z_phot

#_____________________________________________________________________________
def hits_en_z_up():

    #energy along the z position of the hit in up spectrometer detector

    zpos = -36500 # mm
    zbin = 0.3 # cm
    zmax = 2 # cm
    zmin = -36 # cm

    ebin = 0.3
    emin = 0
    emax = 20

    can = ut.box_canvas()
    hEnZ = ut.prepare_TH2D("hEnZ", zbin, zmin, zmax, ebin, emin, emax)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("up", tree)
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

#hits_en_z_up

#_____________________________________________________________________________
def hits_en_z_down():

    #energy along the z position of the hit in down spectrometer detector

    zpos = -36500 # mm
    zbin = 0.3 # cm
    zmax = 2 # cm
    zmin = -36 # cm

    ebin = 0.3
    emin = 0
    emax = 20

    can = ut.box_canvas()
    hEnZ = ut.prepare_TH2D("hEnZ", zbin, zmin, zmax, ebin, emin, emax)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits("down", tree)
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

#hits_en_z_down

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()




















