#!/usr/bin/python3

import ROOT as rt
from ROOT import gROOT, gSystem

#_____________________________________________________________________________
def main():

    #geometry
    geo = rt.GeoParser("../../config/pro2/geom_pro2.in")
    #geo = rt.GeoParser("../../config/pro2/vacuum_pro2.in")
    #geo = rt.GeoParser("../../config/pro2/beam_magnets_pro2.in")

    #constants to print
    #con = ["vac_phiT", "vac_phiB", "vac_xB", "vac_xBO", "vac_rQB"]
    con = ["vac_zQB", "vac_xQB", "vac_zB", "vac_xB"]
    #con = ["vac_tag2_xBO", "vac_tag1_end_xBO", "vac_tag1_end_xBI", "vac_tag1_xWA", "vac_tag1_xBO"]
    #con = ["B2eR_Theta", "B2eR_Length", "Q3eR_Theta", "Q3eR_Length"]
    #con = ["vac_rBP", "vac_zBTI", "vac_xBTI"]

    for i in con:
        print(i+":", geo.GetConst(i))

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/include")
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4")
    gROOT.ProcessLine(".L ../../src/GeoParser.cxx+")

    gROOT.SetBatch()

    main()

