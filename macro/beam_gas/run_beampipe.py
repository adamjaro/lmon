#!/usr/bin/python3

from ROOT import TFile

from rcalc import rcalc

#_____________________________________________________________________________
def main():

    #input
    infile = "../../lmon.root"

    #output
    outfile = "rc_z0.root"

    rate = rcalc()
    rate.open_input(infile)
    rate.create_output(outfile)

    rate.event_loop()



#_____________________________________________________________________________
if __name__ == "__main__":

    main()


