
#event in tagger with ParticleCounterHits

from ctypes import c_double

import ROOT as rt
from ROOT import gROOT, TMath

from ParticleCounterHits import ParticleCounterHits

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
        geo = rt.GeoParser(cf.str("geom"))

        #connect the input tree
        self.tree = tree
        name = cf.str("name")
        #tagger hits
        self.hits = ParticleCounterHits(name, tree)
        self.hits.local_from_geo(geo, cf.str("geom_shape"))
        #event quantities
        self.inp_el_theta = c_double(0)
        self.inp_el_E = c_double(0)
        self.inp_Q2 = c_double(0)
        self.tree.SetBranchAddress("true_el_theta", self.inp_el_theta)
        self.tree.SetBranchAddress("true_el_E", self.inp_el_E)
        self.tree.SetBranchAddress("true_Q2", self.inp_Q2)

    #__init__

    #_____________________________________________________________________________
    def read(self, i):

        #read a given event

        self.tree.GetEntry(i)

        #hits loop
        nhsel = 0
        for ihit in range(self.hits.GetN()):

            hit = self.hits.GetHit(ihit)
            hit.GlobalToLocal()

            nhsel += 1

        #just one selected hit, miss otherwise
        if nhsel != 1: return False

        #hit quantities
        self.hit_x = hit.x
        self.hit_y = hit.y
        self.hit_E = hit.en

        #event quantities
        self.true_el_theta = self.inp_el_theta.value
        self.true_el_E = self.inp_el_E.value
        self.true_Q2 = self.inp_Q2.value
        #derived quantities
        self.true_mlt = -TMath.Log10(TMath.Pi()-self.inp_el_theta.value)
        self.true_lq = TMath.Log10(self.inp_Q2.value)

        return True

    #read

















