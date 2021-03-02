#!/usr/bin/python

import ROOT as rt
from ROOT import gROOT, TFile, AddressOf

#_____________________________________________________________________________
def main(basedir=None):

    #production directory
    if basedir is None:
        basedir = ".."

    #input
    infile = basedir + "/lmon_120.root"

    #output
    outfile = basedir + "/HCal.csv"

    #lmon input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #load the tree
    gROOT.ProcessLine("struct EntryD {Double_t v;};")
    hcal_edep_EM = rt.EntryD()
    hcal_edep_HAD = rt.EntryD()
    tree.SetBranchAddress("hcal_edep_EM", AddressOf(hcal_edep_EM, "v"))
    tree.SetBranchAddress("hcal_edep_HAD", AddressOf(hcal_edep_HAD, "v"))

    #output txt csv
    out = open(outfile, "write")
    out.write("hcal_edep_EM,hcal_edep_HAD\n")

    #event loop
    for iev in xrange(tree.GetEntriesFast()):

        tree.GetEntry(iev)

        out.write(str(hcal_edep_EM.v)+","+str(hcal_edep_HAD.v)+"\n")

    out.close()



#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()









