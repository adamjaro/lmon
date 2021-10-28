#!/usr/bin/python3

from ctypes import c_double

from ROOT import gROOT, TFile

#_____________________________________________________________________________
def main():

    inp = TFile.Open("../../lmon.root")
    tree = inp.Get("DetectorTree")

    power_W = c_double(0)
    flux_photon_per_s = c_double(0)
    tree.SetBranchAddress("power_W", power_W)
    tree.SetBranchAddress("flux_photon_per_s", flux_photon_per_s)

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)

        print("flux_photon_per_s", flux_photon_per_s.value)

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()

