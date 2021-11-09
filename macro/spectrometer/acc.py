#!/usr/bin/python3

from ctypes import c_double, c_bool, c_int

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree
from ROOT import std

#from EventStore import EventStore

import sys
sys.path.append('../')
import plot_utils as ut

from ParticleCounterHits import ParticleCounterHits

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = acc_spec
    func[1] = up_rate

    func[101] = load_lmon
    #func[102] = load_dd

    func[iplot]()

#main

#_____________________________________________________________________________
def acc_spec():

    emin = 0
    emax = 19

    amax = 0.06

    inp_lmon = TFile.Open("lmon.root")
    tree_lmon = inp_lmon.Get("event")

    acc_lmon = rt.acc_Q2_kine(tree_lmon, "gen_en", "is_spect")
    acc_lmon.prec = 0.08
    acc_lmon.delt = 1e-2
    #acc_lmon.bmin = 0.1
    #acc_lmon.nev = int(1e5)
    gLmon = acc_lmon.get()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, 0, emax, amax)

    ut.put_yx_tit(frame, "Acceptance", "Photon energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gLmon, rt.kBlue)
    gLmon.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_spec

#_____________________________________________________________________________
def up_rate():

    #plot range
    xybin = 10
    xylen = 200

    inp_lmon = TFile.Open("lmon.root")
    #tree = inp_lmon.Get("up")
    tree = inp_lmon.Get("down")

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xylen, xylen, xybin, -xylen, xylen)

    tree.Draw("y:x >> hXY")

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    ytit = "#it{y} (mm)"
    xtit = "#it{x} (mm)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#up_rate

#_____________________________________________________________________________
def load_lmon():

    emin = 1.

    #input
    inp = TFile.Open("../../lmon.root")

    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = 100000

    #input generated particles
    pdg = std.vector(int)()
    en = std.vector(float)()
    tree.SetBranchAddress("gen_pdg", pdg)
    tree.SetBranchAddress("gen_en", en)

    #spectrometer hits
    up_hits = ParticleCounterHits("up", tree)
    up_hits.ypos = 142. # mm
    down_hits = ParticleCounterHits("down", tree)
    down_hits.ypos = -142. # mm

    #outputs
    out = TFile("lmon.root", "recreate")
    otree = TTree("event", "event")
    gen_en = c_double(0)
    up_en = c_double(0)
    down_en = c_double(0)
    is_spect = c_bool(0)
    otree.Branch("gen_en", gen_en, "gen_en/D")
    otree.Branch("up_en", up_en, "up_en/D")
    otree.Branch("down_en", down_en, "down_en/D")
    otree.Branch("is_spect", is_spect, "is_spect/O")

    up_hits.CreateOutput("up")
    down_hits.CreateOutput("down")

    #event loop
    if nev<0: nev = tree.GetEntries()
    for ievt in range(nev):
        tree.GetEntry(ievt)

        gen_en.value = 0.
        up_en.value = 0.
        down_en.value = 0.
        is_spect.value = 0

        #generated photon energy
        for imc in range(pdg.size()):
            if pdg.at(imc) == 22: gen_en.value = en.at(imc)

        #print(gen_en.value)

        #spectrometer hits
        for i in range(up_hits.GetN()):
            hit = up_hits.GetHit(i)
            hit.LocalY()

            up_en.value += hit.en
            up_hits.FillOutput()

        for i in range(down_hits.GetN()):
            hit = down_hits.GetHit(i)
            hit.LocalY()

            down_en.value += hit.en
            down_hits.FillOutput()

        #coincidence selection
        if up_en.value > emin and down_en.value > emin:
            is_spect.value = 1

        otree.Fill()

    #event loop

    otree.Write()
    up_hits.otree.Write()
    down_hits.otree.Write()
    out.Close()

    print("load_lmon done")

#load_lmon

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()



