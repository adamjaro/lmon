#!/usr/bin/python

#print generator information

import ROOT as rt
from ROOT import gROOT, TFile, AddressOf, std

#_____________________________________________________________________________
def main():

    inp = TFile.Open("../lmon.root")
    tree = inp.Get("DetectorTree")

    #tree.Print()

    gen_pdg = std.vector(int)()
    gen_en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", gen_pdg)
    tree.SetBranchAddress("gen_en", gen_en)

    tree.GetEntry(0)

    ngen = gen_pdg.size()

    for i in range(ngen):

        print i, gen_pdg.at(i), gen_en.at(i)







#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()


