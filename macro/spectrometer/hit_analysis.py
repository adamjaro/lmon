#!/usr/bin/python3

from ctypes import c_double, c_bool, c_int
from sys import stdout

import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree, TDatabasePDG, TF1
from ROOT import std

#from EventStore import EventStore

import sys
sys.path.append('../')
import plot_utils as ut

from ParticleCounterHits import ParticleCounterHits

#_____________________________________________________________________________
def main():

    emin = 1.

    #infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax2/lmon.root"
    #outfile = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax2/hits.root"

    #infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1b/lmon.root"
    #outfile = "/home/jaroslav/sim/lmon/data/luminosity/lm1b/hits.root"

    #infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1c/lmon.root"
    #outfile = "/home/jaroslav/sim/lmon/data/luminosity/lm1c/hits.root"

    #input
    inp = TFile.Open(infile)

    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = -12

    #input generated particles
    pdg = std.vector(int)()
    en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", pdg)
    tree.SetBranchAddress("gen_en", en)

    #spectrometer hits
    up_hits = ParticleCounterHits("up", tree)
    up_hits.ypos = 163.524 # mm
    down_hits = ParticleCounterHits("down", tree)
    down_hits.ypos = -163.524 # mm

    #photon detector hits
    phot_hits = ParticleCounterHits("phot", tree)

    #outputs
    out = TFile(outfile, "recreate")

    #interaction tree
    otree = TTree("event", "event")
    gen_en = c_double(0)
    up_en = c_double(0)
    down_en = c_double(0)
    is_spect = c_bool(0)
    phot_en = c_double(0)
    otree.Branch("gen_en", gen_en, "gen_en/D")
    otree.Branch("up_en", up_en, "up_en/D")
    otree.Branch("down_en", down_en, "down_en/D")
    otree.Branch("is_spect", is_spect, "is_spect/O")
    otree.Branch("phot_en", phot_en, "phot_en/D")

    #hit trees
    up_hits.CreateOutput("up")
    down_hits.CreateOutput("down")
    phot_hits.CreateOutput("phot")
    phot_hits.zpos = -37175 # mm

    #bunch crossing tree
    btree = TTree("bunch", "bunch")
    bun_ni = c_int(0)
    bun_up_en = c_double(0)
    bun_down_en = c_double(0)
    bun_phot_en = c_double(0)
    btree.Branch("bun_ni", bun_ni, "bun_ni/I")
    btree.Branch("bun_up_en", bun_up_en, "bun_up_en/D")
    btree.Branch("bun_down_en", bun_down_en, "bun_down_en/D")
    btree.Branch("bun_phot_en", bun_phot_en, "bun_phot_en/D")

    #Poisson distribution for bunch crossings
    lam = get_scale(1)["lambda"]
    print("Lambda:", lam)
    fPois = TF1("Pois", "TMath::Power([0], Int_t(TMath::Floor(x)) )*TMath::Exp(-[0])/TMath::Factorial( Int_t(TMath::Floor(x)) )", 0, 12.*lam)
    fPois.SetParameter(0, lam)

    #print("Pois:", fPois.GetRandom())

    #number of interactions in bunch crossing
    nI = int(TMath.Floor(fPois.GetRandom()))
    bun_ni.value = nI

    #interaction loop
    if nev<0: nev = tree.GetEntries()
    iprint = int(nev/12)

    for ievt in range(nev):
        tree.GetEntry(ievt)

        if ievt%iprint == 0 and ievt>0:
            print("{0:.1f} %".format(100.*ievt/nev))
            stdout.flush()

        gen_en.value = 0.
        up_en.value = 0.
        down_en.value = 0.
        is_spect.value = 0
        phot_en.value = 0.

        #generated photon energy
        for imc in range(pdg.size()):
            if pdg.at(imc) == 22: gen_en.value = en.at(imc)

        #print(gen_en.value)

        #spectrometer hits
        for i in range(up_hits.GetN()):
            hit = up_hits.GetHit(i)
            hit.LocalY()

            up_en.value += hit.en
            up_hits.FillOutput()

        for i in range(down_hits.GetN()):
            hit = down_hits.GetHit(i)
            hit.LocalY()

            down_en.value += hit.en
            down_hits.FillOutput()

        #coincidence selection
        if up_en.value > emin and down_en.value > emin:
            is_spect.value = 1

        #photon hits
        for i in range(phot_hits.GetN()):
            hit = phot_hits.GetHit(i)
            hit.GlobalToLocal()

            phot_en.value += hit.en
            phot_hits.FillOutput()

        otree.Fill()

        #bunch crossing
        if nI == 0:
            btree.Fill()

            nI = int(TMath.Floor(fPois.GetRandom()))
            bun_ni.value = nI

            bun_up_en.value = 0.
            bun_down_en.value = 0.
            bun_phot_en.value = 0.

        else:
            nI -= 1

            bun_up_en.value += up_en.value
            bun_down_en.value += down_en.value
            bun_phot_en.value += phot_en.value

    #interaction loop

    otree.Write()
    up_hits.otree.Write()
    down_hits.otree.Write()
    phot_hits.otree.Write()
    btree.Write()
    out.Close()

    print("Hit analysis done")

#main

#_____________________________________________________________________________
def get_scale(Ni):

    #scale for event rate in Hz per one simulated interaction
    #Ni is number of simulated interactions

    #interaction cross section, mb
    sigma_tot = 171.29 # 18x275
    #sigma_tot = 123.83 # 10x100
    #sigma_tot = 79.18 # 5x41

    #instantaneous luminosity, cm^-2 sec^-1
    lumi_cmsec = 1.54e33 # 18x275
    #lumi_cmsec = 4.48e33 # 10x100
    #lumi_cmsec = 0.44e33 # 5x41

    #number of bunches
    nbunch = 290 # 18x275
    #nbunch = 1160 # 10x100
    #nbunch = 1160 # 5x41

    #electron beam energy, GeV
    #Ee = 18. # GeV
    #Ee = 10. # GeV
    Ee = 5. # GeV

    #collider circumference, speed of light, electron mass
    circ = 3834. # m
    cspeed = 299792458. # m sec^-1
    me = TDatabasePDG.Instance().GetParticle(11).Mass() # GeV

    #beam velocity (units of c)
    beta = np.sqrt(Ee**2-me**2)/Ee
    print("Beta:", beta)
    print("Orbit period (micro sec):", 1e6*circ/(beta*cspeed))

    #bunch spacing, sec
    Tb = circ/(beta*cspeed*nbunch)
    print("Bunch spacing (micro sec):", 1e6*Tb)
    print("Bunch frequency (MHz):", 1e-6/Tb)

    #luminosity per bunch crossing, mb^-1
    Lb = lumi_cmsec*1e-27*Tb
    print("Luminosity per bunch crossing, mb^-1:", Lb)
    print("Mean number of interactions per bunch crossing:", sigma_tot*Lb)
    print("Probability for at least one interaction in bunch crossing:", (1.-np.e**(-sigma_tot*Lb)))

    scale = {}
    scale["lambda"] = sigma_tot*Lb
    scale["Tb"] = Tb # sec

    #rate per one simulated interaction, Hz
    #return (1./Ni)*sigma_tot*1e-27*lumi_cmsec

    return scale

#get_scale

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

















