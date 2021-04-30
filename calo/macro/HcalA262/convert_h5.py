#!/usr/bin/python

#convert ROOT to DataFrame

import ROOT as rt
from ROOT import gROOT, TFile, AddressOf, std

from pandas import DataFrame, HDFStore

#_____________________________________________________________________________
def main():

    #beam = [3, 5, 7, 10, 20, 30, 50, 75]
    #beam = [6, 8, 12, 16, 25, 32, 64]
    beam = [3, 5, 7, 10, 20, 30, 50, 75] # 1.5, 2, 
    #abso_z = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]

    #data directory
    basedir = "/home/jaroslav/sim/hcal/data/hcal3e1"

    gROOT.ProcessLine("struct EntryD {Double_t v;};")

    for i in beam:

        run_convert(basedir, i)

    print "All done"

#_____________________________________________________________________________
def run_convert(basedir, beam):

    print "Converting for:", beam

    infile = basedir + "/lmon_en"+str(beam)+".root"
    outfile = basedir + "/HCal_en"+str(beam)+".h5"
    #infile = basedir + "/lmon_a"+str(beam)+".root"
    #outfile = basedir + "/HCal_a"+str(beam)+".h5"

    #lmon input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #load the tree
    hcal_edep_EM = rt.EntryD()
    hcal_edep_HAD = rt.EntryD()
    hcal_edep_layers = std.vector(float)()
    ecal_edep = rt.EntryD()
    tree.SetBranchAddress("hcal_edep_EM", AddressOf(hcal_edep_EM, "v"))
    tree.SetBranchAddress("hcal_edep_HAD", AddressOf(hcal_edep_HAD, "v"))
    tree.SetBranchAddress("hcal_edep_layers", hcal_edep_layers)
    tree.SetBranchAddress("ecal_edep", AddressOf(ecal_edep, "v"))

    tree.GetEntry(0)
    nlay = hcal_edep_layers.size()

    #output DataFrame
    col = ["ecal_edep", "hcal_edep_EM", "hcal_edep_HAD"]
    lnam = {}
    for i in range(nlay):
        n = "hcal_edep_layer"+str(i)
        lnam[i] = n
        col.append(n)

    df_inp = []

    #event loop
    for iev in xrange(tree.GetEntriesFast()):

        tree.GetEntry(iev)

        lin = []
        lin.append(ecal_edep.v)
        lin.append(hcal_edep_EM.v)
        lin.append(hcal_edep_HAD.v)

        for i in xrange(nlay):

            lin.append(hcal_edep_layers.at(i))

        df_inp.append(lin)

    df = DataFrame(df_inp, columns=col)

    print df

    out = HDFStore(outfile)
    out["hcal"] = df
    out.close()

    inp.Close()

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()









