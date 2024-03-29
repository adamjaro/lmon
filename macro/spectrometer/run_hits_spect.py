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
    from ParticleCounterSpect import ParticleCounterSpect
    hits = ParticleCounterSpect()

    #inputs
    indir = "/home/jaroslav/sim/lmon"
    inlist = glob(indir+"/lmon.root")

    # 18x275 GeV
    #hits.sigma_tot = 171.29 # mb
    #hits.lumi_cmsec = 1.54e33 # cm^-2 sec^-1
    #hits.nbunch = 290
    #hits.Ee = 18. # GeV

    # 5x41 GeV
    hits.sigma_tot = 79.18 # mb
    hits.lumi_cmsec = 0.44e33 # cm^-2 sec^-1
    hits.nbunch = 1160
    hits.Ee = 5. # GeV

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
    sys.path.append(lmon_top+"/macro/spectrometer")

    gSystem.AddIncludePath(" -I"+lmon_top+"/include")
    gSystem.AddIncludePath(" -I"+geant_inst)
    gROOT.ProcessLine(".L "+lmon_top+"/src/GeoParser.cxx+")

#add_path

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()












