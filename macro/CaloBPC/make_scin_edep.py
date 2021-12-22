
import ROOT as rt
from ROOT import addressof, TTree, TFile, TChain, gROOT, std

#_____________________________________________________________________________
def make_scin_edep(inlist, outfile):

    #input
    tree = TChain("DetectorTree")
    for i in inlist:
        tree.Add(i)

    scin_istrip = std.vector(int)()
    scin_ilay = std.vector(int)()
    scin_edep = std.vector(float)()

    tree.SetBranchAddress("bpc_scin_istrip", scin_istrip)
    tree.SetBranchAddress("bpc_scin_ilay", scin_ilay)
    tree.SetBranchAddress("bpc_scin_edep", scin_edep)

    #output txt csv
    out = open(outfile, "w")
    out.write("bpc_edep\n")

    #event loop
    nev = tree.GetEntries()
    for ievt in range(nev):
        tree.GetEntry(ievt)

        #deposited energy in event
        edep = 0.

        #scintillator loop
        for iscin in range(scin_edep.size()):

            #print(iscin, scin_istrip.at(iscin), scin_ilay.at(iscin), scin_edep.at(iscin))
            edep += scin_edep.at(iscin)

        out.write(str(edep)+"\n")

    out.close()

    print("Done")






