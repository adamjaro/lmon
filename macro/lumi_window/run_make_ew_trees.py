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
    from make_ew_trees import make_ew_trees

    #inputs
    indir = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax2"
    inlist = glob(indir+"/lmon.root")

    make_ew_trees(inlist, "ew.root")

#_____________________________________________________________________________
def add_path(lmon_top):

    sys.path.append(lmon_top+"/macro")
    sys.path.append(lmon_top+"/macro/lumi_window")

#add_path

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()













