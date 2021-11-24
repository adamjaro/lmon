#!/usr/bin/python3

from ROOT import gROOT, TFile

#_____________________________________________________________________________
def main():

    #infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1a/hits.root"
    infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1ax1/hits.root"

    trees = ["event", "bunch", "phot", "up", "down"]

    inp = TFile.Open(infile)

    print(infile)
    print("    Counts in hit trees:")
    for i in trees:

        print("    {0:7s}".format(i), inp.Get(i).GetEntries())

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()

