#!/usr/bin/python

import ROOT as rt
from ROOT import gROOT, TFile

#_____________________________________________________________________________
def main():

    #infile = "../data/lmon_18x275_all_0p5Mevt.root"
    #infile = "../data/lmon_18x275_all_0p25T_100kevt.root"
    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_1Mevt.root"
    infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_NoFilter_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qd_beff2_5Mevt.root"

    #sigma_BH = 129.6 # mb
    sigma_BH = 276.346654276 # mb, zeus 0.1 GeV
    #sigma_BH = 0.0538 # mb, qr_Qd

    lumi = 1.45e6 # mb^-1 s^-1

    emin = 1. # GeV


    gROOT.SetBatch()

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #tree.Print()
    #return

    #all simulated events
    nall = get_count(tree)

    #photon detector counts
    #nphot = get_count(tree, "phot_en>"+str(emin*1e3))
    nphot = get_count(tree, "phot_en>"+str(emin))

    #up detector
    #nup = get_count(tree, "up_en>"+str(emin*1e3))
    nup = get_count(tree, "up_en>"+str(emin))

    #down detector
    #ndown = get_count(tree, "down_en>"+str(emin*1e3))
    ndown = get_count(tree, "down_en>"+str(emin))

    #spectromter coincidence
    #sel = "up_en>"+str(emin*1e3)+" && down_en>"+str(emin*1e3)
    sel = "up_en>"+str(emin)+" && down_en>"+str(emin)
    nspec = get_count(tree, sel)

    #print nall, nphot, nup, ndown, nspec

    #tagger 1
    nlow1 = get_count(tree, "lowQ2s1_en>"+str(emin))

    #tagger 2
    nlow2 = get_count(tree, "lowQ2s2_en>"+str(emin))

    print "Input:", infile
    print "sigma_BH:", sigma_BH, "mb"
    print "L:", lumi, "mb^-1 s^-1"
    print "emin:", emin, "GeV"
    print "nall:", nall

    #photon detector rate
    get_rate(sigma_BH, lumi, nall, nphot, "phot")

    #up detector rate
    get_rate(sigma_BH, lumi, nall, nup, "up")

    #down detector rate
    get_rate(sigma_BH, lumi, nall, ndown, "down")

    #coincidence rate
    get_rate(sigma_BH, lumi, nall, nspec, "pair")
    
    #tagger1 rate
    get_rate(sigma_BH, lumi, nall, nlow1, "tagger 1")

    #tagger2 rate
    get_rate(sigma_BH, lumi, nall, nlow2, "tagger 2")

    #print nlow1, nlow2

# main

#_____________________________________________________________________________
def get_count(t, sel=""):

    #event count from a tree 't' based on selection formula 'sel'

    return float(t.Draw("", sel))

# get_count

#_____________________________________________________________________________
def get_rate(sig, L, nall, nsel, msg=""):

    #print event rate with cross section 'sig', luminosity 'L'
    #and efficiency from 'nall' and 'nsel', show with message 'msg'

    if nsel<=0: return

    print
    print msg+":"
    print "  nsel:", nsel

    #efficiency and Binomial error
    from math import sqrt
    epsilon = nsel/nall
    epsilon_err = epsilon * sqrt( (nall-nsel) / (nall*nsel) )

    #print "sig:", sig
    #print "L:", L
    print "  epsilon:", epsilon, "+/-", epsilon_err


    #        sigma = eff*sqrt( (ngen-nsel) / (ngen*nsel) )

    f = sig * L * epsilon

    print "  f:", f*1e-6, "MHz"

#_____________________________________________________________________________
if __name__ == "__main__":

    main()




















