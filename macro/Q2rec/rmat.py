
#reconstruction matrix Rijk

from sys import stdout
from glob import glob

from ROOT import TFile, TH1D, TChain

import sys
sys.path.append('../')
from TagV2Evt import TagV2Evt
from read_con import read_con

from tjk import tjk

#_____________________________________________________________________________
class rmat:
    #_____________________________________________________________________________
    def __init__(self, config=None, infile=None):

        #create the Rijk
        if infile is None:
            self.init_create(config)

        #load the Rijk
        if infile is not None:
            self.init_load(infile)

    #_____________________________________________________________________________
    def init_create(self, config):

        #create the Rijk

        #configuration
        cf = read_con(config)

        #load the input
        inlist = glob(cf.str("inp_Rijk"))
        tree = TChain("DetectorTree")
        for i in inlist:
            tree.Add(i)

        #open the output
        out = TFile(cf.str("out_Rijk"), "recreate")

        #energy intervals in 'i'
        print("Intervals in 'i'")
        hEi = TH1D("hEi", "hEi", cf.int("nen"), cf("emin"), cf("emax"))
        tree.Draw("true_el_E >> hEi")

        #energy for events in tagger for underflow and overflow
        hEiTag = TH1D("hEiTag", "hEiTag", cf.int("nen"), cf("emin"), cf("emax"))

        #angles at positions in 'j' and 'k'
        tjks = {}
        for i in range(1, hEi.GetNbinsX()+1):
            #print(i, hEi.GetBinLowEdge(i), hEi.GetBinLowEdge(i)+hEi.GetBinWidth(i))

            tjks[i] = tjk(i, cf)

        #number of events
        nev = cf.int("nev")
        if nev < 0: nev = tree.GetEntries()

        #event loop
        iprint = int(nev/12)
        evt = TagV2Evt(tree, cf)
        print("Event loop")
        for iev in range(nev):

            if iev%iprint == 0:
                print("{0:.1f} %".format(100.*iev/nev))
                stdout.flush()

            #read the event
            if not evt.read(iev): continue

            #print(evt.hit_x, evt.hit_y, evt.true_el_E, evt.true_mlt)

            #energy index 'i' in Rijk
            i = hEi.FindBin(evt.true_el_E)
            if i < 1 or i > hEi.GetNbinsX(): continue

            #energy underflow and overflow
            hEiTag.Fill(evt.true_el_E)

            #fill element of Rijk at a given 'i'
            tjks[i].fill(evt.hit_x, evt.hit_y, evt.true_mlt)

        #projections for mean mlt at each 'j' and 'k'
        print("Projections at 'j' and 'k'")
        stdout.flush()
        for i in tjks:
            tjks[i].make_proj()

        #print underflow and overflow
        self.print_uo(hEiTag, tjks)

        #write the individual parts of Rijk
        hEi.Write()
        hEiTag.Write()
        for i in tjks:
            tjks[i].write()

        out.Close()

        print("All done")

    #_____________________________________________________________________________
    def init_load(self, infile):

        #load the Rijk from input file

        #open the input
        self.inp = TFile.Open(infile, "read")

        #energy intervals in 'i'
        self.hEi = self.inp.Get("hEi")

        #angles at positions in 'j' and 'k'
        self.tjks = {}
        for i in range(1, self.hEi.GetNbinsX()+1):
            #print i, hEi.GetBinLowEdge(i), hEi.GetBinLowEdge(i)+hEi.GetBinWidth(i)

            self.tjks[i] = tjk(i, inp=self.inp)

            #print self.tjks[i].hTjk

    #init_load

    #_____________________________________________________________________________
    def print_uo(self, hEi, tjks):

        #print underflow and overflow

        print("Underflow and overflow:")
        print("  E:", hEi.GetEntries(), hEi.GetBinContent(0), hEi.GetBinContent(hEi.GetNbinsX()+1))

        for i in tjks:
            tjks[i].print_uo()




























