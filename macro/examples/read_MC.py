#!/usr/bin/env python

#example macro to read the MC particles

from ROOT import gROOT, TFile, std

#_____________________________________________________________________________
def main():

    #open the input
    inp = TFile.Open("../../data/lmon.root")
    tree = inp.Get("DetectorTree")

    #get the branches for MC particle
    pdg = std.vector(int)()
    px = std.vector(float)()
    py = std.vector(float)()
    pz = std.vector(float)()
    en = std.vector(float)()

    tree.SetBranchAddress("gen_pdg", pdg)
    tree.SetBranchAddress("gen_px", px)
    tree.SetBranchAddress("gen_py", py)
    tree.SetBranchAddress("gen_pz", pz)
    tree.SetBranchAddress("gen_en", en)

    ievt = 2 # event number to read

    #load the event
    tree.GetEntry(ievt)

    #loop over MC particles, all vectors are of the same size
    for i in xrange(pdg.size()):

        print i, pdg.at(i), px.at(i), py.at(i), pz.at(i), en.at(i)

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()


