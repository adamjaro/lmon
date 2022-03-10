#!/usr/bin/python3

from ROOT import gROOT, TFile, std

#_____________________________________________________________________________
def main():

    inp = TFile.Open("../../lmon.root")
    tree = inp.Get("DetectorTree")

    gen_pdg = std.vector(int)()
    gen_en = std.vector(float)()
    gen_vx = std.vector(float)()
    gen_vy = std.vector(float)()
    gen_vz = std.vector(float)()

    tree.SetBranchAddress("gen_pdg", gen_pdg)
    tree.SetBranchAddress("gen_en", gen_en)
    tree.SetBranchAddress("gen_vx", gen_vx)
    tree.SetBranchAddress("gen_vy", gen_vy)
    tree.SetBranchAddress("gen_vz", gen_vz)

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)

        print("Next MC event:", i)

        for ip in range(gen_pdg.size()):

            print("  mc particle:", gen_pdg.at(ip), gen_en.at(ip), gen_vx.at(ip), gen_vy.at(ip), gen_vz.at(ip))

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()



