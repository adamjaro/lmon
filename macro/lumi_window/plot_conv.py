#!/usr/bin/python3

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem
from ROOT import addressof, TTree, std

from ew_hits import ew_hits

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2
    funclist = []
    funclist.append( make_conv_tree ) # 0
    funclist.append( phot_en_conv ) # 1
    funclist.append( conv_prob_en ) # 2
    funclist.append( clean_conv_en ) # 3

    funclist[iplot]()

#main

#_____________________________________________________________________________
def make_conv_tree():

    #input
    #inp = TFile.Open("../../lmon.root")
    inp = TFile.Open("../../data/ew/ew1b.root")
    #inp = TFile.Open("../../data/ew/ew1c.root")
    #inp = TFile.Open("../../data/ew/ew1d.root")
    #inp = TFile.Open("../../data/ew/ew1e.root")
    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = -1

    #output
    out = TFile("conv_b.root", "recreate")
    gROOT.ProcessLine( "struct EntryF {Float_t v;};" )
    gROOT.ProcessLine( "struct EntryB {Bool_t v;};" )
    gen_en = rt.EntryF()
    conv = rt.EntryB()
    clean = rt.EntryB()
    adep = rt.EntryF()
    otree = TTree("conv_tree", "conv_tree")
    otree.Branch("gen_en", addressof(gen_en, "v"), "gen_en/F")
    otree.Branch("conv", addressof(conv, "v"), "conv/O")
    otree.Branch("clean", addressof(clean, "v"), "clean/O")
    otree.Branch("adep", addressof(adep, "v"), "adep/F")

    #exit window hits
    hits = ew_hits("ew", tree)

    #generated particles
    pdg = std.vector(int)()
    en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", pdg)
    tree.SetBranchAddress("gen_en", en)

    if nev<0: nev = tree.GetEntries()
    for ievt in range(nev):
        tree.GetEntry(ievt)

        #print("Next event")

        #generated photon energy
        gen_en.v = -1.
        for imc in range(pdg.size()):
            if pdg.at(imc) == 22: gen_en.v = en.at(imc)

        #conversion in the event
        conv.v = False

        #all secondaries and deposited energy in event
        asec = 0
        adep.v = 0.

        for ihit in range(hits.get_n()):

            hit = hits.get_hit(ihit)
            hit.global_to_zpos(-18644) # mm

            #print(hit.pdg, hit.prim, hit.conv, hit.nsec, hit.edep, hit.en)

            #conversion in the event
            if hit.prim == 1 and hit.conv == 1: conv.v = True

            #all secondaries and deposited energy
            asec += hit.nsec
            adep.v += hit.edep

        #evaluate clean conversion
        clean.v = False
        if conv.v and asec == 2: clean.v = True

        #print(conv.v, clean.v, adep.v, gen_en.v)

        otree.Fill()

    otree.Write()
    out.Close()

#make_conv_tree

#_____________________________________________________________________________
def phot_en_conv():

    #photon energy with conversions or clean conversions

    #plot range
    emin = 0
    emax = 19
    ebin = 0.1

    inp = TFile.Open("conv.root")
    tree = inp.Get("conv_tree")

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    nev = tree.Draw("gen_en >> hE")
    #nev = tree.Draw("gen_en >> hE", "conv==1")
    #nev = tree.Draw("gen_en >> hE", "clean==1")

    print(nev)

    ut.line_h1(hE)

    ut.put_yx_tit(hE, "Counts", "#it{E} (GeV)")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.01)

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phot_en_conv

#_____________________________________________________________________________
def conv_prob_en():

    #conversion probability as a function of photon energy

    #plot range
    emin = 0
    emax = 19
    pmin = 0.01
    #pmax = 0.3
    pmax = 1

    inp = TFile.Open("conv_b.root")
    tree = inp.Get("conv_tree")

    prec = 0.01
    calc = rt.conv_calc(tree, prec, 1e-6)
    #calc.nev = 500000

    conv = calc.get_conv()

    calc.conv_in_all = True
    calc.clean_in_sel = True
    clean = calc.get_conv()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, pmin, emax, pmax)

    ut.put_yx_tit(frame, "Conversion probability", "#it{E}_{#gamma} (GeV)")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.01)

    frame.Draw()
    gPad.SetGrid()

    ut.set_graph(conv, rt.kBlue)
    conv.Draw("psame")

    ut.set_graph(clean, rt.kRed)
    clean.Draw("psame")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#conv_prob_en

#_____________________________________________________________________________
def clean_conv_en():

    #fraction of clean conversions as a function of photon energy

    #plot range
    emin = 0
    emax = 19
    pmin = 0
    pmax = 1.1

    inp = TFile.Open("conv.root")
    tree = inp.Get("conv_tree")

    prec = 0.01
    calc = rt.conv_calc(tree, prec, 1e-6)
    #calc.nev = 300000
    calc.conv_in_all = True
    calc.clean_in_sel = True

    conv = calc.get_conv()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, pmin, emax, pmax)

    ut.put_yx_tit(frame, "Fraction of clean conversions", "#it{E}_{#gamma} (GeV)")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.01)

    frame.Draw()
    gPad.SetGrid()

    ut.set_graph(conv, rt.kBlue)
    conv.Draw("psame")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#clean_conv_en

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L conv_calc.cxx+")

    main()















