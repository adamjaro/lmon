#!/usr/bin/python3

import sys
from glob import glob

import ROOT as rt
from ROOT import gROOT, gSystem

#_____________________________________________________________________________
def main():

    #lmon
    lmon_top = "/home/jaroslav/sim/lmon"

    add_path(lmon_top)
    from make_scin_edep import make_scin_edep

    #inputs
    indir = "."
    inlist = glob(indir+"/lmon.root")

    make_scin_edep(inlist, "bpc.csv")

#_____________________________________________________________________________
def add_path(lmon_top):

    sys.path.append(lmon_top+"/macro")
    sys.path.append(lmon_top+"/macro/CaloBPC")

#add_path

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()















