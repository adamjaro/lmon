
#Hit analysis for taggers

from ctypes import c_double, c_bool, c_int
from sys import stdout

import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TChain, TFile, gSystem
from ROOT import TGraph, TMath, TTree, TDatabasePDG, TF1
from ROOT import std

from ParticleCounterHits import ParticleCounterHits

#_____________________________________________________________________________
class ParticleCounterTag:
    #_____________________________________________________________________________
    def __init__(self):

        #input
        self.tree = TChain("DetectorTree")

        #geometry
        self.geo = None

        #output file name
        self.outfile = "hits_tag.root"

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

        #tagger hits
        tag1_hits = ParticleCounterHits("lowQ2s1", self.tree)
        tag2_hits = ParticleCounterHits("lowQ2s2", self.tree)
        tag1_hits.local_from_geo(self.geo, "Tagger1box")
        tag2_hits.local_from_geo(self.geo, "Tagger2box")

        #outputs
        print("Output name:", self.outfile)
        out = TFile(self.outfile, "recreate")

        #interaction tree
        otree = TTree("event", "event")
        gen_en = c_double(0)
        s1_IsHit = c_bool(0)
        s2_IsHit = c_bool(0)
        otree.Branch("gen_en", gen_en, "gen_en/D")
        otree.Branch("s1_IsHit", s1_IsHit, "s1_IsHit/O")
        otree.Branch("s2_IsHit", s2_IsHit, "s2_IsHit/O")

        #hit trees
        tag1_hits.CreateOutput("s1")
        tag2_hits.CreateOutput("s2")

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

            #generated electron energy
            for imc in range(pdg.size()):
                if pdg.at(imc) == 11: gen_en.value = en.at(imc)

            #tagger hit in event
            s1_IsHit.value = 0
            s2_IsHit.value = 0

            #Tagger 1
            if tag1_hits.GetN() > 0:
                s1_IsHit.value = 1

            tag1_hits.LoopInLocal()

            #Tagger 2
            if tag2_hits.GetN() > 0:
                s2_IsHit.value = 1

            tag2_hits.LoopInLocal()

            otree.Fill()

        #interaction loop

        otree.Write()
        tag1_hits.otree.Write()
        tag2_hits.otree.Write()

        self.print_stat(out)
        out.Close()

        print("Tagger hit analysis done")

    #event_loop

    #_____________________________________________________________________________
    def print_stat(self, out):

        trees = ["event", "s1", "s2"]

        print("Counts in tagger hit trees:")
        for i in trees:

            print("{0:7s}".format(i), out.Get(i).GetEntries())

    #print_stat





















