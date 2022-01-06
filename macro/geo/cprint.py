#!/usr/bin/python3

import ROOT as rt
from ROOT import gROOT, gSystem

#_____________________________________________________________________________
def main():

    #geometry
    geo = rt.GeoParser("../../config/pro2/vacuum_pro2.in")

    print(geo.GetConst("vac_phiQ"))

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/include")
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4")
    gROOT.ProcessLine(".L ../../src/GeoParser.cxx+")

    gROOT.SetBatch()

    main()

