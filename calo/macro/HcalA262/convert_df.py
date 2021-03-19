#!/usr/bin/python

#convert ROOT to DataFrame

import ROOT as rt
from ROOT import gROOT, TFile, AddressOf, std

from pandas import DataFrame

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

    tree.GetEntry(0)
    nlay = hcal_edep_layers.size()

    #output DataFrame
    col = ["hcal_edep_EM", "hcal_edep_HAD"]
    lnam = {}
    for i in range(nlay):
        n = "hcal_edep_layer"+str(i)
        lnam[i] = n
        col.append(n)

    df = DataFrame(columns=col)

    #event loop
    for iev in xrange(tree.GetEntriesFast()):

        tree.GetEntry(iev)

        #print hcal_edep_EM.v, hcal_edep_HAD.v

        df.loc[iev+1, "hcal_edep_EM"] = hcal_edep_EM.v
        df.loc[iev+1, "hcal_edep_HAD"] = hcal_edep_HAD.v

        for i in xrange(nlay):
            #print "i", i, hcal_edep_layers.at(i)

            df.loc[iev+1, lnam[i]] = hcal_edep_layers.at(i)

    #print df

    df.to_csv(outfile)



#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()









