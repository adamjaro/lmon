#!/usr/bin/python3

from ROOT import TFile

from rcalc import rcalc

#_____________________________________________________________________________
def main():

    #input
    infile = "../../lmon.root"

    #output
    outfile = "rc.root"

    rate = rcalc("vtx_tracker")
    #rate.set_rmin(30) # mm
    rate.open_input(infile)
    rate.create_output(outfile)

    rate.event_loop()



#_____________________________________________________________________________
if __name__ == "__main__":

    main()


