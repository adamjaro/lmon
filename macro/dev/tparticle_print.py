#!/usr/bin/python3

from ROOT import gROOT, TFile, TClonesArray

#_____________________________________________________________________________
def main():

    infile = "~/sim/GETaLM/cards/lgen_18x275.root"
    #infile = "input_2.root"

    inp = TFile.Open(infile)
    tree = inp.Get("ltree")

    part = TClonesArray("TParticle")
    tree.SetBranchAddress("particles", part)

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)

        print("Next event:", i)

        for ip in range(part.GetEntries()):
            p = part.At(ip)

            print("  particle:", p.GetPdgCode(), p.Energy(), p.Vx(), p.Vy(), p.Vz())

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()

