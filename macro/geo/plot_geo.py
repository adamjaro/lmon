#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TCanvas

import sys
sys.path.append('../')
import plot_utils as ut

from segment import segment

#_____________________________________________________________________________
def main():

    zmin = -40000.
    zmax = 0.
    xmin = -1200.
    xmax = 800.

    c1 = TCanvas("c1","c1",1000,700)
    frame = gPad.DrawFrame(zmin, xmin, zmax, xmax) # xmin, ymin, xmax, ymax in ROOT
    frame.SetTitle(";Length #it{z} (mm);Horizontal #it{x} (mm)")
    siz = 0.035
    frame.SetTitleSize(siz)
    frame.SetLabelSize(siz)
    frame.SetTitleSize(siz, "Y")
    frame.SetLabelSize(siz, "Y")

    frame.GetYaxis().SetTitleOffset(1)
    frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetYaxis().CenterTitle()
    frame.GetXaxis().CenterTitle()
    gPad.SetLeftMargin(0.07)
    gPad.SetRightMargin(0.01)
    gPad.SetTopMargin(0.02)
    gPad.SetBottomMargin(0.09)

    #geometry
    geo = rt.GeoParser("../../config/geom_all.in")

    #Tagger1
    tag1 = segment("Tagger1box", geo)
    tag1.draw()

    #Tagger2
    tag2 = segment("Tagger2box", geo)
    tag2.draw()

    #Luminosity exit window
    ew = segment("ExitWinBox", geo)
    ew.draw()

    #up spectrometer
    up = segment("LumiSUbox", geo)
    up.draw()

    #Luminosity direct photon detector
    phot = segment("LumiDbox", geo)
    phot.draw()

    #print(geo.GetTopName())

    #print(geo.GetD("LumiSUbox", "dx"))

    gPad.SetGrid()

    ut.invert_col(gPad)
    c1.SaveAs("01fig.pdf")

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/include")
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4")
    gROOT.ProcessLine(".L ../../src/GeoParser.cxx+")

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetFrameLineWidth(2)

    main()


























