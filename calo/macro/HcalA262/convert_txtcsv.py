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
    hcal_edep_EM = rt.EntryD()
    hcal_edep_HAD = rt.EntryD()
    hcal_edep_layers = std.vector(float)()
    tree.SetBranchAddress("hcal_edep_EM", AddressOf(hcal_edep_EM, "v"))
    tree.SetBranchAddress("hcal_edep_HAD", AddressOf(hcal_edep_HAD, "v"))
    tree.SetBranchAddress("hcal_edep_layers", hcal_edep_layers)

    #output txt csv
    out = open(outfile, "write")

    #file header
    tree.GetEntry(0)
    nlay = hcal_edep_layers.size()

    col = ["hcal_edep_EM", "hcal_edep_HAD"]
    for i in range(nlay):
        col.append( "hcal_edep_layer"+str(i) )

    strcol = ""
    for i in col:
        strcol += ","+i

    out.write(strcol+"\n")

    #event loop
    for iev in xrange(tree.GetEntriesFast()):

        tree.GetEntry(iev)

        lin = str(iev+1)
        lin += ","+str(hcal_edep_EM.v)
        lin += ","+str(hcal_edep_HAD.v)

        for i in xrange(nlay):
            lin += ","+str(hcal_edep_layers.at(i))

        out.write(lin+"\n")

    out.close()

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()









