#!/usr/bin/python3

#run the reconstruction

import sys

from ROOT import gROOT, gSystem

#_____________________________________________________________________________
def main(args):

    #lmon and Geant
    lmon_top = "/home/jaroslav/sim/lmon"
    geant_inst = "/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4"

    add_path(lmon_top, geant_inst)
    from reconstruct import reconstruct

    #name of config file from command line argument
    if len(args) < 2:
        print("No configuration specified.")
        quit()
    args.pop(0)
    config = args.pop(0)

    #init and run
    reconstruct(config)

#main

#_____________________________________________________________________________
def add_path(lmon_top, geant_inst):

    sys.path.append(lmon_top+"/macro")
    sys.path.append(lmon_top+"/macro/Q2rec")

    gSystem.AddIncludePath(" -I"+lmon_top+"/include")
    gSystem.AddIncludePath(" -I"+geant_inst)
    gROOT.ProcessLine(".L "+lmon_top+"/src/GeoParser.cxx+")

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main(sys.argv)



