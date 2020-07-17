#!/usr/bin/python

#detector acceptance in terms of cross section 

import ROOT as rt
from ROOT import gROOT, TFile

#_____________________________________________________________________________
def main():

    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_1Mevt.root"
    infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_NoFilter_1Mevt.root"

    sigma_gen = 276.346654276 # mb, total cross section of generated sample

    lumi = 0.074 # mb^-1, luminosity per bunch crossing

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #all simulated events
    nall = get_count(tree)
    print "nall", nall

    #condition for detected event
    #cond = "lowQ2s1_IsHit == 1"
    #cond = "lowQ2s2_IsHit == 1"
    #cond = "lowQ2s2_en > 0.1"
    #cond = "phot_en > 0.1"
    cond = "up_en > 0.1 && down_en > 0.1"

    nsel = get_count(tree, cond)
    print "nsel", nsel

    #cross section seen by the detector
    sigma_det = sigma_gen*nsel/nall
    print "sigma_det", sigma_det, "mb"

    #average hits in the detector
    nhits = lumi*sigma_det
    print "nhits", nhits


#_____________________________________________________________________________
def get_count(t, sel=""):

    #event count from a tree 't' based on selection formula 'sel'

    return float(t.Draw("", sel))

# get_count

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()


