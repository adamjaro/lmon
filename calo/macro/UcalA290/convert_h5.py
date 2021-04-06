#!/usr/bin/python

#convert ROOT to DataFrame

import ROOT as rt
from ROOT import gROOT, TFile, AddressOf, std

from pandas import DataFrame, HDFStore

#_____________________________________________________________________________
def main():

    #beam = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10]
    #beam += [20, 30, 50, 75, 100]
    beam = [0.5, 1, 2, 5, 10, 30, 75]
    #beam += [100, 50, 20, 7, 3, 1.5, 0.75]

    #data directory
    basedir = "/home/jaroslav/sim/hcal/data/ucal1a1x17"

    gROOT.ProcessLine("struct EntryD {Double_t v;};")

    for i in beam:

        run_convert(basedir, i)

    print "Done with the conversion"

#_____________________________________________________________________________
def run_convert(basedir, beam):

    print "Converting for:", beam

    infile = basedir + "/lmon_p"+str(beam)+".root"
    outfile = basedir + "/HCal_p"+str(beam)+".h5"

    #lmon input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #load the tree
    ucal_edep_EMC = rt.EntryD()
    ucal_edep_HAC1 = rt.EntryD()
    ucal_edep_HAC2 = rt.EntryD()
    ucal_edep_layers = std.vector(float)()
    tree.SetBranchAddress("ucal_edep_EMC", AddressOf(ucal_edep_EMC, "v"))
    tree.SetBranchAddress("ucal_edep_HAC1", AddressOf(ucal_edep_HAC1, "v"))
    tree.SetBranchAddress("ucal_edep_HAC2", AddressOf(ucal_edep_HAC2, "v"))
    tree.SetBranchAddress("ucal_edep_layers", ucal_edep_layers)

    tree.GetEntry(0)
    nlay = ucal_edep_layers.size()

    #output DataFrame
    col = ["ucal_edep_EMC", "ucal_edep_HAC1", "ucal_edep_HAC2"]
    for i in range(nlay):
        col.append( "ucal_edep_layer"+str(i) )

    df_inp = []

    #event loop
    for iev in xrange(tree.GetEntriesFast()):

        tree.GetEntry(iev)

        lin = []
        lin.append(ucal_edep_EMC.v)
        lin.append(ucal_edep_HAC1.v)
        lin.append(ucal_edep_HAC2.v)

        for i in xrange(nlay):

            lin.append(ucal_edep_layers.at(i))

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









