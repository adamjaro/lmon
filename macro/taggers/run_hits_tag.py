#!/usr/bin/python3

import sys
from glob import glob

import ROOT as rt
from ROOT import gROOT, gSystem

#_____________________________________________________________________________
def main():

    #lmon and Geant
    lmon_top = "/home/jaroslav/sim/lmon"
    geant_inst = "/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4"

    add_path(lmon_top, geant_inst)
    from ParticleCounterTag import ParticleCounterTag
    hits = ParticleCounterTag()

    #inputs
    indir = "/home/jaroslav/sim/lmon"
    inlist = glob(indir+"/lmon.root")

    #geometry
    hits.geo = rt.GeoParser("../../config/geom_all.in")

    #output
    #hits.outfile = indir+"/hits_spect.root"

    #add the inputs and run
    for i in inlist:
        hits.add_input(i)

    hits.event_loop()

    print("All done")

#main

#_____________________________________________________________________________
def add_path(lmon_top, geant_inst):

    sys.path.append(lmon_top+"/macro")
    sys.path.append(lmon_top+"/macro/taggers")

    gSystem.AddIncludePath(" -I"+lmon_top+"/include")
    gSystem.AddIncludePath(" -I"+geant_inst)
    gROOT.ProcessLine(".L "+lmon_top+"/src/GeoParser.cxx+")

#add_path

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()









