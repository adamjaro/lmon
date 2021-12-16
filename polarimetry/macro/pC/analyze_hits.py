#!/usr/bin/python3

from ctypes import c_float

from ROOT import gROOT, TFile, TTree, std, TDatabasePDG

#_____________________________________________________________________________
def main():

    #input
    inp = TFile.Open("pC.root")
    tree = inp.Get("DetectorTree")

    #input generated particles
    gen_pdg = std.vector(int)()
    gen_en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", gen_pdg)
    tree.SetBranchAddress("gen_en", gen_en)

    #layer hits
    lay10_hit_edep = std.vector(float)()
    lay11_hit_edep = std.vector(float)()
    lay12_hit_edep = std.vector(float)()
    lay13_hit_edep = std.vector(float)()
    lay20_hit_edep = std.vector(float)()
    lay21_hit_edep = std.vector(float)()
    lay22_hit_edep = std.vector(float)()
    lay23_hit_edep = std.vector(float)()
    tree.SetBranchAddress("lay10_HitEdep", lay10_hit_edep)
    tree.SetBranchAddress("lay11_HitEdep", lay11_hit_edep)
    tree.SetBranchAddress("lay12_HitEdep", lay12_hit_edep)
    tree.SetBranchAddress("lay13_HitEdep", lay13_hit_edep)
    tree.SetBranchAddress("lay20_HitEdep", lay20_hit_edep)
    tree.SetBranchAddress("lay21_HitEdep", lay21_hit_edep)
    tree.SetBranchAddress("lay22_HitEdep", lay22_hit_edep)
    tree.SetBranchAddress("lay23_HitEdep", lay23_hit_edep)

    #output
    out = TFile("events.root", "recreate")
    otree = TTree("event", "event")
    ekin = c_float(0)
    lay10_edep = c_float(0)
    lay11_edep = c_float(0)
    lay12_edep = c_float(0)
    lay13_edep = c_float(0)
    lay20_edep = c_float(0)
    lay21_edep = c_float(0)
    lay22_edep = c_float(0)
    lay23_edep = c_float(0)
    otree.Branch("ekin", ekin, "ekin/F") # kinetic energy, MeV
    otree.Branch("lay10_edep", lay10_edep, "lay10_edep/F") # deposited energy, MeV
    otree.Branch("lay11_edep", lay11_edep, "lay11_edep/F")
    otree.Branch("lay12_edep", lay12_edep, "lay12_edep/F")
    otree.Branch("lay13_edep", lay13_edep, "lay13_edep/F")
    otree.Branch("lay20_edep", lay20_edep, "lay20_edep/F")
    otree.Branch("lay21_edep", lay21_edep, "lay21_edep/F")
    otree.Branch("lay22_edep", lay22_edep, "lay22_edep/F")
    otree.Branch("lay21_edep", lay23_edep, "lay23_edep/F")

    #number of events
    nev = tree.GetEntries()
    #nev = 100000

    #event loop
    for iev in range(nev):
        tree.GetEntry(iev)

        if iev%100000 == 0:
            print("Event: ", iev)

        #deposited energy, MeV
        lay10_edep.value = 0.
        lay11_edep.value = 0.
        lay12_edep.value = 0.
        lay13_edep.value = 0.
        lay20_edep.value = 0.
        lay21_edep.value = 0.
        lay22_edep.value = 0.
        lay23_edep.value = 0.

        #hit loops for layers
        nhit = 0
        nhit += get_edep_lay(lay10_hit_edep, lay10_edep)
        nhit += get_edep_lay(lay11_hit_edep, lay11_edep)
        nhit += get_edep_lay(lay12_hit_edep, lay12_edep)
        nhit += get_edep_lay(lay13_hit_edep, lay13_edep)
        nhit += get_edep_lay(lay20_hit_edep, lay20_edep)
        nhit += get_edep_lay(lay21_hit_edep, lay21_edep)
        nhit += get_edep_lay(lay22_hit_edep, lay22_edep)
        nhit += get_edep_lay(lay23_hit_edep, lay23_edep)

        #events with hits
        if nhit <= 0:
            continue

        #generated kinetic energy, MeV
        egen = gen_en.at(0)
        mass = TDatabasePDG.Instance().GetParticle(gen_pdg.at(0)).Mass()
        ekin.value = (egen-mass)*1e3 # MeV 

        #fill the output tree
        otree.Fill()

    #finish
    otree.Write()
    out.Close()

#main

#_____________________________________________________________________________
def get_edep_lay(hit_edep, edep):

    #hit loop
    for ihit in range(hit_edep.size()):
        edep.value += hit_edep.at(ihit)*1e3 # to MeV

    return hit_edep.size()

#get_edep_lay

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()















