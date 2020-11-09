
#event in tagger with BoxCalV2Hits

import ROOT as rt
from ROOT import gROOT, TMath, AddressOf

from BoxCalV2Hits import BoxCalV2Hits

#_____________________________________________________________________________
class TagV2Evt:
    #_____________________________________________________________________________
    def __init__(self, tree, cf):

        #tagger measured quantities
        self.hit_x = 0.
        self.hit_y = 0.
        self.hit_E = 0.

        #generated event quantities
        self.true_el_theta = 0.
        self.true_el_E = 0.
        self.true_Q2 = 0.
        #derived quantities
        self.true_mlt = 0. # -log_10(pi-true_el_theta)
        self.true_lq = 0. # log_10(true_Q2)

        #configuration on tagger geometry
        self.xpos = cf("xpos")
        self.zpos = cf("zpos")
        self.rot_y = cf("rot_y")
        self.zmin = cf("zmin")

        #connect the input tree
        self.tree = tree
        name = cf.str("name")
        #tagger hits
        self.hits = BoxCalV2Hits(name, tree)
        #event quantities
        gROOT.ProcessLine("struct EntryTagV2 {Double_t v;};")
        self.inp_el_theta = rt.EntryTagV2()
        self.inp_el_E = rt.EntryTagV2()
        self.inp_Q2 = rt.EntryTagV2()
        self.tree.SetBranchAddress("true_el_theta", AddressOf(self.inp_el_theta, "v"))
        self.tree.SetBranchAddress("true_el_E", AddressOf(self.inp_el_E, "v"))
        self.tree.SetBranchAddress("true_Q2", AddressOf(self.inp_Q2, "v"))

    #__init__

    #_____________________________________________________________________________
    def read(self, i):

        #read a given event

        self.tree.GetEntry(i)

        #hits loop
        nhsel = 0
        for ihit in xrange(self.hits.GetN()):

            hit = self.hits.GetHit(ihit)
            hit.GlobalToLocal(self.xpos, 0, self.zpos, self.rot_y)

            if hit.z < self.zmin: continue

            nhsel += 1

        #just one selected hit, miss otherwise
        if nhsel != 1: return False

        #hit quantities
        self.hit_x = hit.x
        self.hit_y = hit.y
        self.hit_E = hit.en

        #event quantities
        self.true_el_theta = self.inp_el_theta.v
        self.true_el_E = self.inp_el_E.v
        self.true_Q2 = self.inp_Q2.v
        #derived quantities
        self.true_mlt = -TMath.Log10(TMath.Pi()-self.inp_el_theta.v)
        self.true_lq = TMath.Log10(self.inp_Q2.v)

        return True

    #read

















