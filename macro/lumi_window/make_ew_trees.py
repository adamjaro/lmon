
import ROOT as rt
from ROOT import addressof, TTree, TFile, TChain, gROOT, std

from ew_hits import ew_hits

#_____________________________________________________________________________
def make_ew_trees(inlist, outfile):

    #input
    tree = TChain("DetectorTree")
    for i in inlist:
        tree.Add(i)

    #output
    out = TFile(outfile, "recreate")
    gROOT.ProcessLine( "struct EntryF {Float_t v;};" )
    gROOT.ProcessLine( "struct EntryB {Bool_t v;};" )

    #hits by primary photons
    x = rt.EntryF()
    y = rt.EntryF()
    z = rt.EntryF()
    en = rt.EntryF()
    otree = TTree("prim_tree", "prim_tree")
    otree.Branch("x", addressof(x, "v"), "x/F")
    otree.Branch("y", addressof(y, "v"), "y/F")
    otree.Branch("z", addressof(z, "v"), "z/F")
    otree.Branch("en", addressof(en, "v"), "en/F")

    #conversions
    gen_en = rt.EntryF()
    conv = rt.EntryB()
    clean = rt.EntryB()
    adep = rt.EntryF()
    conv_tree = TTree("conv_tree", "conv_tree")
    conv_tree.Branch("gen_en", addressof(gen_en, "v"), "gen_en/F")
    conv_tree.Branch("conv", addressof(conv, "v"), "conv/O")
    conv_tree.Branch("clean", addressof(clean, "v"), "clean/O")
    conv_tree.Branch("adep", addressof(adep, "v"), "adep/F")

    #input hits
    hits = ew_hits("ew", tree)

    #input generated particles
    inp_pdg = std.vector(int)()
    inp_en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", inp_pdg)
    tree.SetBranchAddress("gen_en", inp_en)

    #event loop
    nev = tree.GetEntries()
    for ievt in range(nev):
    #for ievt in range(12):
        tree.GetEntry(ievt)

        #print("Next event")

        #generated photon energy
        gen_en.v = -1.
        for imc in range(inp_pdg.size()):
            if inp_pdg.at(imc) == 22: gen_en.v = inp_en.at(imc)

        #primary photon
        was_prim = False

        #conversion in the event
        conv.v = False

        #all secondaries and deposited energy in event
        asec = 0
        adep.v = 0.

        #hit loop
        for ihit in range(hits.get_n()):

            hit = hits.get_hit(ihit)

            hit.global_to_zpos(-18500) # mm

            #hit by primary photon
            if hit.prim != 0 and hit.pdg == 22 and was_prim != True:

                was_prim = True

                x.v = hit.x
                y.v = hit.y
                z.v = hit.z
                en.v = hit.en

                otree.Fill()

            #conversion in the event
            if hit.prim == 1 and hit.conv == 1: conv.v = True

            #all secondaries and deposited energy
            asec += hit.nsec
            adep.v += hit.edep

        #hit loop

        #evaluate clean conversion
        clean.v = False
        if conv.v and asec == 2: clean.v = True

        conv_tree.Fill()

    #event loop

    otree.Write()
    conv_tree.Write()
    out.Close()









