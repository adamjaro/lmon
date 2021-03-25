#!/usr/bin/python

#conversion to csv where DataFrame is not available

import ROOT as rt
from ROOT import gROOT, TFile, AddressOf, std

#_____________________________________________________________________________
def main(basedir=None):

    #production directory
    if basedir is None:
        basedir = ".."

    #input
    infile = basedir + "/lmon.root"

    #output
    outfile = basedir + "/HCal.csv"

    #lmon input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #load the tree
    gROOT.ProcessLine("struct EntryD {Double_t v;};")
    ucal_edep_EMC = rt.EntryD()
    ucal_edep_HAC1 = rt.EntryD()
    ucal_edep_HAC2 = rt.EntryD()
    ucal_edep_layers = std.vector(float)()
    tree.SetBranchAddress("ucal_edep_EMC", AddressOf(ucal_edep_EMC, "v"))
    tree.SetBranchAddress("ucal_edep_HAC1", AddressOf(ucal_edep_HAC1, "v"))
    tree.SetBranchAddress("ucal_edep_HAC2", AddressOf(ucal_edep_HAC2, "v"))
    tree.SetBranchAddress("ucal_edep_layers", ucal_edep_layers)

    #output txt csv
    out = open(outfile, "write")

    #file header
    tree.GetEntry(0)
    nlay = ucal_edep_layers.size()

    col = ["ucal_edep_EMC", "ucal_edep_HAC1", "ucal_edep_HAC2"]
    for i in range(nlay):
        col.append( "ucal_edep_layer"+str(i) )

    strcol = ""
    for i in col:
        strcol += ","+i

    out.write(strcol+"\n")

    #event loop
    for iev in xrange(tree.GetEntriesFast()):

        tree.GetEntry(iev)

        lin = str(iev+1)
        lin += ","+str(ucal_edep_EMC.v)
        lin += ","+str(ucal_edep_HAC1.v)
        lin += ","+str(ucal_edep_HAC2.v)

        for i in xrange(nlay):
            lin += ","+str(ucal_edep_layers.at(i))

        out.write(lin+"\n")

    out.close()

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()









