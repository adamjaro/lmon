#!/usr/bin/python3

import ROOT as rt
from ROOT import gROOT, gSystem, TFile

#_____________________________________________________________________________
def main():

    #include directories
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/include")
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/calo/include")

    #load hit definitions
    gROOT.ProcessLine(".L /home/jaroslav/sim/lmon/calo/src/PhotoHitsV2.cxx+")
    gROOT.ProcessLine(".L /home/jaroslav/sim/lmon/calo/src/CalPWOHits.cxx+")

    #input file
    inp = "/home/jaroslav/sim/lmon/calo/macro/PWO/pwo.root"

    #open the input
    infile = TFile.Open(inp)
    tree = infile.Get("DetectorTree")

    #PMT photocathode hits
    hits_cath = rt.PhotoHitsV2.Coll()
    hits_cath.ConnectInput("pwo_cath", tree)

    #calorimeter cell hits
    hits_cell = rt.CalPWOHits.Coll()
    hits_cell.ConnectInput("pwo", tree)

    #event loop
    for iev in range(tree.GetEntriesFast()):

        tree.GetEntry(iev)

        print("Next event:", iev)

        #load the hits for the current entry
        hits_cath.LoadInput()
        hits_cell.LoadInput()

        print("PMT hits:", hits_cath.GetN())

        #PMT hits loop
        for ihit in range(hits_cath.GetN()):
            hit = hits_cath.GetUnit(ihit)

            print("PhotoHit:", hit.time, hit.pos_x, hit.pos_y, hit.pos_z)

        print("Cell hits:", hits_cell.GetN())

        #cell hits loop
        for ihit in range(hits_cell.GetN()):
            hit = hits_cell.GetUnit(ihit)

            print("CalPWOHit:", hit.cell_id, hit.en)

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()













