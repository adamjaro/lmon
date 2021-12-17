#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TCanvas

import sys
sys.path.append('../')
import plot_utils as ut

from segment import segment
from magnet import magnet
from vacuum import vacuum

#_____________________________________________________________________________
def main():

    #geometry
    geo = rt.GeoParser("../../config/pro2/vacuum_pro2.in")

    print("zQT", geo.GetD("vac_b2b_drift", "zQT"))
    print("xQT", geo.GetD("vac_b2b_drift", "xQT"))
    print("zQB", geo.GetD("vac_b2b_drift", "zQB"))
    print("xQB", geo.GetD("vac_b2b_drift", "xQB"))


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

