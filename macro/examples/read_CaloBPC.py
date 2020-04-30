#!/usr/bin/python

#example macro on reading BPC scintillator signals

from ROOT import gROOT, TFile, std

#_____________________________________________________________________________
def main():

    #open the input
    inp = TFile.Open("../../data/lmon.root")
    tree = inp.Get("DetectorTree")

    #get the branches with scintillator signals
    istrip = std.vector(int)()
    ilay = std.vector(int)()
    edep = std.vector(float)()

    tree.SetBranchAddress("lowQ2_scin_istrip", istrip)
    tree.SetBranchAddress("lowQ2_scin_ilay", ilay)
    tree.SetBranchAddress("lowQ2_scin_edep", edep)

    ievt = 2 # event number to read

    #load the event
    tree.GetEntry(ievt)

    #loop over the scintillators, all vectors are of the same size
    for i in xrange(istrip.size()):

        print i, ilay.at(i), istrip.at(i), edep.at(i)

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()


