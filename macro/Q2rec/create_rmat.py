#!/usr/bin/python

#create the reconstruction matrix Rijk

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))+"/../")

from ROOT import gROOT

from rmat import rmat

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

    #init and run
    rmat(config)

