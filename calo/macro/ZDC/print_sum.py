#!/usr/bin/python3

from ctypes import c_double

from ROOT import gROOT, TFile

#_____________________________________________________________________________
def main():

    inp = TFile.Open("lmon.root")
    tree = inp.Get("DetectorTree")

    ecal_edep = c_double(0)
    hcal_edep_HAD = c_double(0)
    tree.SetBranchAddress("ecal_edep", ecal_edep)
    tree.SetBranchAddress("hcal_edep_HAD", hcal_edep_HAD)

    ecal_sum = 0.
    hcal_sum = 0.

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)

        ecal_sum += ecal_edep.value
        hcal_sum += hcal_edep_HAD.value

    print("ecal_sum:", ecal_sum)
    print("hcal_sum:", hcal_sum)

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()

