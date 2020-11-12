#!/usr/bin/python

#run the reconstruction

import sys
from sys import stdout
sys.path.append('../')

import ROOT as rt
from ROOT import gROOT, gSystem, TFile, TTree, AddressOf, TMath

from rmat import rmat
from read_con import read_con
from TagV2Evt import TagV2Evt

#_____________________________________________________________________________
def main(cf):

    #input reconstruction matrix Rijk
    mat = rmat(infile=cf.str("inp_rec_Rijk"))

    #input data for reconstruction
    inp = TFile.Open(cf.str("inp_rec_data"), "read")
    tree = inp.Get("DetectorTree")

    #output from reconstruction
    out = TFile(cf.str("out_rec"), "recreate")
    rec_tree = TTree("Q2rec", "Q2rec")

    #set the output tree
    gROOT.ProcessLine("struct Entry {Double_t v;};")
    true_Q2 = make_branch("true_Q2", rec_tree, rt.Entry)
    true_el_E = make_branch("true_el_E", rec_tree, rt.Entry)
    true_el_theta = make_branch("true_el_theta", rec_tree, rt.Entry)
    true_mlt = make_branch("true_mlt", rec_tree, rt.Entry)
    true_lq = make_branch("true_lq", rec_tree, rt.Entry)

    hit_x = make_branch("hit_x", rec_tree, rt.Entry)
    hit_y = make_branch("hit_y", rec_tree, rt.Entry)
    hit_E = make_branch("hit_E", rec_tree, rt.Entry)
    rec_mlt = make_branch("rec_mlt", rec_tree, rt.Entry)
    rec_Q2 = make_branch("rec_Q2", rec_tree, rt.Entry)
    rec_lq = make_branch("rec_lq", rec_tree, rt.Entry)

    #number of events
    nev = cf.int("nev")
    if nev < 0: nev = tree.GetEntries()

    #range in mlt
    mlt_range = [cf("tmin"), cf("tmax")]

    print "Event loop, events:", nev
    iprint = nev/12
    evt = TagV2Evt(tree, cf)
    for iev in xrange(nev):

        if iev%iprint == 0:
            print 100*iev/nev, "%"
            stdout.flush()

        #read the event
        if not evt.read(iev): continue

        #input true values
        true_lq.v = evt.true_lq

        #energy index 'i'
        i = mat.hEi.FindBin(evt.hit_E)
        if i < 1 or i > mat.hEi.GetNbinsX(): continue

        #mlt at 'j' and 'k'
        jk = mat.tjks[i].hTjk.FindBin(evt.hit_x, evt.hit_y)
        #print jk
        mlt = mat.tjks[i].hTjk.GetBinContent( jk )
        if mlt < mlt_range[0] or mlt > mlt_range[1]:
            continue

        #electron scattering angle
        theta = 10**(-mlt)
        #print theta

        #reconstructed Q^2
        rec_Q2.v = 2.*18*evt.hit_E*(1. - TMath.Cos(theta))
        rec_lq.v = TMath.Log10(rec_Q2.v)
        #print rec_lq.v, true_lq.v


        #print mlt, evt.true_mlt

        rec_tree.Fill()

    rec_tree.Write()
    out.Close()

    print "All done"

#_____________________________________________________________________________
def make_branch(name, tree, entry, dat="D"):

    #create tree branch of a given data type

    x = entry()
    x.v = 0
    tree.Branch(name, AddressOf(x, "v"), name+"/"+dat)

    return x

#make_branch

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    #name of config file from command line argument
    args = sys.argv
    if len(args) < 2:
        print "No configuration specified."
        quit()
    args.pop(0)
    config = args.pop(0)
    cf = read_con(config)

    #init and run
    main(cf)

    #beep when done
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")


