
#Hit analysis for luminosity spectrometer

from ctypes import c_double, c_bool, c_int
from sys import stdout

import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TChain, TFile, gSystem
from ROOT import TGraph, TMath, TTree, TDatabasePDG, TF1
from ROOT import std

from ParticleCounterHits import ParticleCounterHits

#_____________________________________________________________________________
class ParticleCounterSpect:
    #_____________________________________________________________________________
    def __init__(self):

        #interaction cross section, mb
        self.sigma_tot = 0.

        #instantaneous luminosity, cm^-2 sec^-1
        self.lumi_cmsec = 0.

        #number of bunches
        self.nbunch = 0.

        #electron beam energy, GeV
        self.Ee = 0.

        #coincidence selection
        self.emin = 1. # GeV

        #collider circumference, speed of light, electron mass
        self.circ = 3834. # m
        self.cspeed = 299792458. # m sec^-1
        self.me = TDatabasePDG.Instance().GetParticle(11).Mass() # GeV

        #input
        self.tree = TChain("DetectorTree")

        #geometry
        self.geo = None

        #output file name
        self.outfile = "hits_spect.root"

    #_____________________________________________________________________________
    def add_input(self, infile):

        self.tree.Add(infile)

    #_____________________________________________________________________________
    def event_loop(self, nev = -1):

        #nev is number of events to analyze, negative for all

        #input generated particles
        pdg = std.vector(int)()
        en = std.vector(float)()
        self.tree.SetBranchAddress("gen_pdg", pdg)
        self.tree.SetBranchAddress("gen_en", en)

        #spectrometer hits
        up_hits = ParticleCounterHits("up", self.tree)
        up_hits.local_from_geo(self.geo, "LumiSUbox")

        down_hits = ParticleCounterHits("down", self.tree)
        down_hits.local_from_geo(self.geo, "LumiSDbox")

        #photon detector hits
        phot_hits = ParticleCounterHits("phot", self.tree)
        phot_hits.local_from_geo(self.geo, "LumiDbox")

        #flow counters hits
        ew_front_hits = ParticleCounterHits("cnt_ew_front", self.tree)
        ew_rear_hits = ParticleCounterHits("cnt_ew_rear", self.tree)
        mag_front_hits = ParticleCounterHits("cnt_mag_front", self.tree)
        mag_rear_hits = ParticleCounterHits("cnt_mag_rear", self.tree)
        ew_front_hits.local_from_geo(self.geo, "ExitWinBox")
        ew_rear_hits.local_from_geo(self.geo, "ExitWinBox")
        mag_front_hits.local_from_geo(self.geo, "lumi_dipole")
        mag_rear_hits.local_from_geo(self.geo, "lumi_dipole")

        #outputs
        out = TFile(self.outfile, "recreate")

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

        #hit trees for flow counters
        ew_front_hits.CreateOutput("ew_front")
        ew_rear_hits.CreateOutput("ew_rear")
        mag_front_hits.CreateOutput("mag_front")
        mag_rear_hits.CreateOutput("mag_rear")

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
        lam = self.get_scale()["lambda"]
        print("Lambda:", lam)
        fPois = TF1("Pois", "TMath::Power([0], Int_t(TMath::Floor(x)) )\
            *TMath::Exp(-[0])/TMath::Factorial( Int_t(TMath::Floor(x)) )", 0, 12.*lam)
        fPois.SetParameter(0, lam)

        #number of interactions in bunch crossing
        nI = int(TMath.Floor(fPois.GetRandom()))
        bun_ni.value = nI

        #print period
        if nev < 0: nev = self.tree.GetEntries()
        iprint = int(nev/12)

        #interaction loop
        for ievt in range(nev):
            self.tree.GetEntry(ievt)

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

            #flow counters hits
            ew_front_hits.LoopInLocal()
            ew_rear_hits.LoopInLocal()
            mag_front_hits.LoopInLocal()
            mag_rear_hits.LoopInLocal()

            #spectrometer hits
            for i in range(up_hits.GetN()):
                hit = up_hits.GetHit(i)
                hit.GlobalToLocal()

                up_en.value += hit.en
                up_hits.FillOutput()

            for i in range(down_hits.GetN()):
                hit = down_hits.GetHit(i)
                hit.GlobalToLocal()

                down_en.value += hit.en
                down_hits.FillOutput()

            #coincidence selection
            if up_en.value > self.emin and down_en.value > self.emin:
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
        ew_front_hits.otree.Write()
        ew_rear_hits.otree.Write()
        mag_front_hits.otree.Write()
        mag_rear_hits.otree.Write()
        btree.Write()
        self.print_stat(out)
        out.Close()

        print("Hit analysis done")

    #event_loop

    #_____________________________________________________________________________
    def get_scale(self):

        #beam velocity (units of c)
        beta = np.sqrt(self.Ee**2-self.me**2)/self.Ee
        print("Beta:", beta)
        print("Orbit period (micro sec):", 1e6*self.circ/(beta*self.cspeed))

        #bunch spacing, sec
        Tb = self.circ/(beta*self.cspeed*self.nbunch)
        print("Bunch spacing (micro sec):", 1e6*Tb)
        print("Bunch frequency (MHz):", 1e-6/Tb)

        #luminosity per bunch crossing, mb^-1
        Lb = self.lumi_cmsec*1e-27*Tb
        print("Luminosity per bunch crossing, mb^-1:", Lb)
        print("Mean number of interactions per bunch crossing:", self.sigma_tot*Lb)
        print("Probability for at least one interaction in bunch crossing:", (1.-np.e**(-self.sigma_tot*Lb)))

        scale = {}
        scale["lambda"] = self.sigma_tot*Lb
        scale["Tb"] = Tb # sec

        return scale

    #get_scale

    #_____________________________________________________________________________
    def print_stat(self, out):

        trees = ["event", "bunch", "phot", "up", "down"]
        trees += ["ew_front", "ew_rear", "mag_front", "mag_rear"]

        print("    Counts in hit trees:")
        for i in trees:

            print("    {0:7s}".format(i), out.Get(i).GetEntries())

    #print_stat
















