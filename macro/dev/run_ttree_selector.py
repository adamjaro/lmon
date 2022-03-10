#!/usr/bin/python3

from ttree_selector import ttree_selector

#_____________________________________________________________________________
def main():

    #input file
    infile = "~/sim/GETaLM/cards/lgen_18x275.root"

    #number of events per input
    nev = 5

    #selector for inputs
    sel = ttree_selector(infile)

    for i in range(3):

        sel.get_n(nev, "input_"+str(i)+".root")

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    main()

