#!/usr/bin/python3

from ctypes import c_double, c_bool, c_int
import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree, TDatabasePDG, TF1
from ROOT import std

#from EventStore import EventStore

import sys
sys.path.append('../')
import plot_utils as ut

from ParticleCounterHits import ParticleCounterHits

#_____________________________________________________________________________
def main():

    iplot = 3

    func = {}
    func[0] = acc_spec
    func[1] = up_rate
    func[2] = en_bun
    func[3] = hit_z

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

    ut.put_yx_tit(frame, "Spectrometer acceptance", "Photon energy #it{E} (GeV)", 1.6, 1.3)

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

    #detector = "up"
    #detector = "down"
    detector = "phot"

    #plot range
    xybin = 5.
    xylen = 110.

    inp_lmon = TFile.Open("lmon.root")
    #number of interactions from event tree
    ni = inp_lmon.Get("event").GetEntries()
    #hits tree
    tree = inp_lmon.Get(detector)

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xylen, xylen, xybin, -xylen, xylen)
    tree.Draw("y:x >> hXY")

    #scale to hits per unit area per second
    scale = get_scale(ni)
    print("scale:", scale)
    lam = scale["lambda"]
    tb = scale["Tb"]

    #bin area in mm^2
    bin_area = xybin**2
    print("area:", bin_area)

    #scale_area = scale/bin_area # mm^-2 sec^-1
    #print("scale_area:", scale_area)

    nhits_all = 0.

    for ix in range(1, hXY.GetNbinsX()+1):
        for iy in range(1, hXY.GetNbinsY()+1):

            nh = hXY.GetBinContent(ix, iy)
            nhits_all += nh

            #hits in bunch crossing
            nhb = (nh/ni)*lam

            #rate per area, mm^-2 sec^-1
            rA = (1.-np.e**(-nhb))*(1./tb)*(1./bin_area)
            #print(rA)

            hXY.SetBinContent(ix, iy, rA)

    #hits per interaction
    print("Hits per interaction:", nhits_all/ni)

    #integrated rate
    rate_all = (1.-np.e**(-(nhits_all/ni)*lam))*(1./tb)
    print("Integrated rate (MHz):", 1e-6*rate_all)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    ytit = "#it{y} (mm)"
    xtit = "#it{x} (mm)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    hXY.SetZTitle("Event rate (mm^{-2} s^{-1})")
    hXY.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.15)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#up_rate

#_____________________________________________________________________________
def en_bun():

    #energy in bunch crossing

    #detector = "bun_up_en"
    #detector = "bun_down_en"
    detector = "bun_phot_en"

    #plot range
    ebin = 0.5
    #emax = 35.
    emax = 150.

    inp_lmon = TFile.Open("lmon.root")
    tree = inp_lmon.Get("bunch")

    can = ut.box_canvas()
    hE = ut.prepare_TH1D("hE", ebin, 0, emax)

    tree.Draw(detector+" >> hE")

    ut.set_H1D_col(hE, rt.kBlue)

    ut.put_yx_tit(hE, "Counts", "Incident energy in bunch crossing (GeV)", 1.5, 1.4)

    ut.set_margin_lbtr(gPad, 0.11, 0.11, 0.02, 0.03)

    gPad.SetGrid()

    gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_bun

#_____________________________________________________________________________
def hit_z():

    #hit z position

    #detector = "up"
    #detector = "down"
    detector = "phot"

    #plot range
    zbin = 1e-3
    zmin = -0.1
    zmax = 0.1

    inp_lmon = TFile.Open("lmon.root")
    tree = inp_lmon.Get(detector)

    can = ut.box_canvas()
    hZ = ut.prepare_TH1D("hZ", zbin, zmin, zmax)

    tree.Draw("z >> hZ")
    print("Entries:", hZ.GetEntries())

    ut.set_H1D_col(hZ, rt.kBlue)

    ut.put_yx_tit(hZ, "Counts", "Hit #it{z} (mm)", 1.5, 1.4)

    ut.set_margin_lbtr(gPad, 0.11, 0.11, 0.02, 0.03)

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hit_z

#_____________________________________________________________________________
def load_lmon():

    emin = 1.

    #input
    inp = TFile.Open("../../lmon.root")
    #inp = TFile.Open("../../lmon_ys1.root")

    tree = inp.Get("DetectorTree")

    #number of events, negative for all
    nev = -100000

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

    #photon detector hits
    phot_hits = ParticleCounterHits("phot", tree)

    #outputs
    out = TFile("lmon.root", "recreate")

    #interaction tree
    otree = TTree("event", "event")
    gen_en = c_double(0)
    up_en = c_double(0)
    down_en = c_double(0)
    is_spect = c_bool(0)
    phot_en = c_double(0)
    otree.Branch("gen_en", gen_en, "gen_en/D")
    otree.Branch("up_en", up_en, "up_en/D")
    otree.Branch("down_en", down_en, "down_en/D")
    otree.Branch("is_spect", is_spect, "is_spect/O")
    otree.Branch("phot_en", phot_en, "phot_en/D")

    #hit trees
    up_hits.CreateOutput("up")
    down_hits.CreateOutput("down")
    phot_hits.CreateOutput("phot")
    phot_hits.zpos = -37000. # mm

    #bunch crossing tree
    btree = TTree("bunch", "bunch")
    bun_ni = c_int(0)
    bun_up_en = c_double(0)
    bun_down_en = c_double(0)
    bun_phot_en = c_double(0)
    btree.Branch("bun_ni", bun_ni, "bun_ni/I")
    btree.Branch("bun_up_en", bun_up_en, "bun_up_en/D")
    btree.Branch("bun_down_en", bun_down_en, "bun_down_en/D")
    btree.Branch("bun_phot_en", bun_phot_en, "bun_phot_en/D")

    #Poisson distribution for bunch crossings
    lam = get_scale(1)["lambda"]
    print("Lambda:", lam)
    fPois = TF1("Pois", "TMath::Power([0], Int_t(TMath::Floor(x)) )*TMath::Exp(-[0])/TMath::Factorial( Int_t(TMath::Floor(x)) )", 0, 12.*lam)
    fPois.SetParameter(0, lam)

    #print("Pois:", fPois.GetRandom())

    #number of interactions in bunch crossing
    nI = int(TMath.Floor(fPois.GetRandom()))
    bun_ni.value = nI

    #interaction loop
    if nev<0: nev = tree.GetEntries()
    for ievt in range(nev):
        tree.GetEntry(ievt)

        gen_en.value = 0.
        up_en.value = 0.
        down_en.value = 0.
        is_spect.value = 0
        phot_en.value = 0.

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

        #photon hits
        for i in range(phot_hits.GetN()):
            hit = phot_hits.GetHit(i)
            hit.GlobalToLocal()

            phot_en.value += hit.en
            phot_hits.FillOutput()

        otree.Fill()

        #bunch crossing
        if nI == 0:
            btree.Fill()

            nI = int(TMath.Floor(fPois.GetRandom()))
            bun_ni.value = nI

            bun_up_en.value = 0.
            bun_down_en.value = 0.
            bun_phot_en.value = 0.

        else:
            nI -= 1

            bun_up_en.value += up_en.value
            bun_down_en.value += down_en.value
            bun_phot_en.value += phot_en.value

    #interaction loop

    otree.Write()
    up_hits.otree.Write()
    down_hits.otree.Write()
    phot_hits.otree.Write()
    btree.Write()
    out.Close()

    print("load_lmon done")

#load_lmon

#_____________________________________________________________________________
def get_scale(Ni):

    #scale for event rate in Hz per one simulated interaction
    #Ni is number of simulated interactions

    #interaction cross section, mb
    sigma_tot = 171.29

    #instantaneous luminosity, cm^-2 sec^-1
    lumi_cmsec = 1.54e33

    #number of bunches
    nbunch = 290

    #electron beam energy, GeV
    Ee = 18. # GeV

    #collider circumference, speed of light, electron mass
    circ = 3834. # m
    cspeed = 299792458. # m sec^-1
    me = TDatabasePDG.Instance().GetParticle(11).Mass() # GeV

    #beam velocity (units of c)
    beta = np.sqrt(Ee**2-me**2)/Ee
    print("Beta:", beta)
    print("Orbit period (micro sec):", 1e6*circ/(beta*cspeed))

    #bunch spacing, sec
    Tb = circ/(beta*cspeed*nbunch)
    print("Bunch spacing (micro sec):", 1e6*Tb)
    print("Bunch frequency (MHz):", 1e-6/Tb)

    #luminosity per bunch crossing, mb^-1
    Lb = lumi_cmsec*1e-27*Tb
    print("Luminosity per bunch crossing, mb^-1:", Lb)
    print("Mean number of interactions per bunch crossing:", sigma_tot*Lb)
    print("Probability for at least one interaction in bunch crossing:", (1.-np.e**(-sigma_tot*Lb)))

    scale = {}
    scale["lambda"] = sigma_tot*Lb
    scale["Tb"] = Tb # sec

    #rate per one simulated interaction, Hz
    #return (1./Ni)*sigma_tot*1e-27*lumi_cmsec

    return scale

#get_scale

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()



