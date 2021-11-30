#!/usr/bin/python3

from ctypes import c_double, c_bool

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree
from ROOT import std

#from EventStore import EventStore

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = hit_en
    func[1] = acc_en_s1_lmon_dd

    func[101] = load_lmon
    func[102] = load_dd

    func[iplot]()

#main

#_____________________________________________________________________________
def acc_en_s1_lmon_dd():

    #acceptance in energy for Tagger 1 by lmon and dd4hep

    inp_lmon = TFile.Open("hits_tag.root")
    tree_lmon = inp_lmon.Get("event")

    #inp_dd = TFile.Open("dd.root")
    #tree_dd = inp_dd.Get("event")

    emin = 0
    emax = 19

    amax = 1

    acc_lmon_s1 = rt.acc_Q2_kine(tree_lmon, "gen_en", "s1_IsHit")
    acc_lmon_s1.prec = 0.1
    #acc_lmon.bmin = 0.1
    #acc_lmon.nev = int(1e5)
    gLmonS1 = acc_lmon_s1.get()

    acc_lmon_s2 = rt.acc_Q2_kine(tree_lmon, "gen_en", "s2_IsHit")
    acc_lmon_s2.prec = 0.1
    gLmonS2 = acc_lmon_s2.get()

    #acc_dd = rt.acc_Q2_kine(tree_dd, "gen_en", "s1_IsHit")
    #acc_dd = rt.acc_Q2_kine(tree_dd, "gen_en", "s2_IsHit")
    #acc_dd.prec = 0.1
    #acc_dd.bmin = 0.1
    #gDD = acc_dd.get()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, 0, emax, amax)

    ut.put_yx_tit(frame, "Acceptance", "Electron energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gLmonS1, rt.kBlue)
    gLmonS1.Draw("psame")

    ut.set_graph(gLmonS2, rt.kRed)
    gLmonS2.Draw("psame")

    #ut.set_graph(gDD, rt.kRed)
    #gDD.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_s1_lmon_dd

#_____________________________________________________________________________
def hit_en():

    #energy in tagger

    #infile = "lmon.root"
    infile = "dd.root"

    emin = 0
    emax = 19
    ebin = 0.1
    #emax = 1.1
    #ebin = 0.01

    inp = TFile.Open(infile)
    tree = inp.Get("event")

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    #nev = tree.Draw("hit_s1_en >> hE", "s1_IsHit==1")
    nev = tree.Draw("hit_s2_en >> hE", "s2_IsHit==1")
    #nev = tree.Draw("hit_s1_en/gen_en >> hE", "s1_IsHit==1")
    #nev = tree.Draw("hit_s2_en/gen_en >> hE", "s2_IsHit==1")
    #nev = tree.Draw("hit_s1_en >> hE", "(s1_IsHit==1)&&((hit_s1_en/gen_en)>0.9)")
    #nev = tree.Draw("hit_s2_en >> hE", "(s2_IsHit==1)&&((hit_s2_en/gen_en)>0.9)")
    print(nev)

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hit_en

#_____________________________________________________________________________
def load_lmon():

    #input
    inp = TFile.Open("../../lmon.root")

    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = -1

    #input generated particles
    pdg = std.vector(int)()
    en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", pdg)
    tree.SetBranchAddress("gen_en", en)

    #input tagger counter hits
    en_s1 = std.vector(float)()
    en_s2 = std.vector(float)()
    tree.SetBranchAddress("lowQ2s1_HitEn", en_s1)
    tree.SetBranchAddress("lowQ2s2_HitEn", en_s2)

    #output
    out = TFile("lmon.root", "recreate")
    otree = TTree("event", "event")
    gen_en = c_double(0)
    hit_s1_en = c_double(0)
    hit_s2_en = c_double(0)
    s1_IsHit = c_bool(0)
    s2_IsHit = c_bool(0)
    otree.Branch("gen_en", gen_en, "gen_en/D")
    otree.Branch("hit_s1_en", hit_s1_en, "hit_s1_en/D")
    otree.Branch("hit_s2_en", hit_s2_en, "hit_s2_en/D")
    otree.Branch("s1_IsHit", s1_IsHit, "s1_IsHit/O")
    otree.Branch("s2_IsHit", s2_IsHit, "s2_IsHit/O")

    #event loop
    if nev<0: nev = tree.GetEntries()
    for ievt in range(nev):
        tree.GetEntry(ievt)

        #generated electron energy
        for imc in range(pdg.size()):
            if pdg.at(imc) == 11: gen_en.value = en.at(imc)

        #tagger hits
        hit_s1_en.value = -1e9
        hit_s2_en.value = -1e9
        s1_IsHit.value = 0
        s2_IsHit.value = 0

        #Tagger 1
        for i in range(en_s1.size()):
            if en_s1.at(i) > hit_s1_en.value: hit_s1_en.value = en_s1.at(i)

        #Tagger 2
        for i in range(en_s2.size()):
            if en_s2.at(i) > hit_s2_en.value: hit_s2_en.value = en_s2.at(i)

        #hit in event
        if hit_s1_en.value > 0: s1_IsHit.value = 1
        if hit_s2_en.value > 0: s2_IsHit.value = 1

        otree.Fill()

    #event loop

    otree.Write()
    out.Close()

#load_lmon

#_____________________________________________________________________________
def load_dd():

    infile = "/home/jaroslav/sim/Athena/athena_particle_counter/output_10k.root"

    store = EventStore([infile])

    #output
    out = TFile("dd.root", "recreate")
    otree = TTree("event", "event")
    gen_en = c_double(0)
    hit_s1_en = c_double(0)
    hit_s2_en = c_double(0)
    s1_IsHit = c_bool(0)
    s2_IsHit = c_bool(0)
    otree.Branch("gen_en", gen_en, "gen_en/D")
    otree.Branch("hit_s1_en", hit_s1_en, "hit_s1_en/D")
    otree.Branch("hit_s2_en", hit_s2_en, "hit_s2_en/D")
    otree.Branch("s1_IsHit", s1_IsHit, "s1_IsHit/O")
    otree.Branch("s2_IsHit", s2_IsHit, "s2_IsHit/O")

    #event loop
    for iev, evt in enumerate(store):

        #print("Next event")

        gen_en.value = -1

        #mc loop
        for imc in store.get("mcparticles"):

            if imc.genStatus() != 1:
                continue

            #generated electron energy
            if imc.pdgID() == 11: gen_en.value = imc.energy()

            #print("mc:", imc.energy(), imc.pdgID(), imc.genStatus(), imc.parents_size())

        #tagger hits
        hit_s1_en.value = -1e9
        hit_s2_en.value = -1e9
        s1_IsHit.value = 0
        s2_IsHit.value = 0

        #Tagger 1
        for ihit in store.get("ParticleCounterS1"):
            #print("hit s1:", ihit.energyDeposit())

            if ihit.energyDeposit()/gen_en.value < 0.9:
                continue

            if ihit.energyDeposit() < hit_s1_en.value:
                continue

            hit_s1_en.value = ihit.energyDeposit()

        #Tagger 2
        for ihit in store.get("ParticleCounterS2"):
            #print("hit s2:", ihit.energyDeposit())

            if ihit.energyDeposit()/gen_en.value < 0.9:
                continue

            if ihit.energyDeposit() < hit_s2_en.value:
                continue

            hit_s2_en.value = ihit.energyDeposit()

        #hit in event
        if hit_s1_en.value > 0: s1_IsHit.value = 1
        if hit_s2_en.value > 0: s2_IsHit.value = 1

        otree.Fill()

    #event loop

    otree.Write()
    out.Close()

#load_dd

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()

















