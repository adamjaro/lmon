#!/usr/bin/python3

from pandas import DataFrame

#_____________________________________________________________________________
def main():

    #lattice input
    infile = "/home/jaroslav/sim/lattice/211020-esr-ir-db64819/210921a-esr-ir6-275-18-db64819.txt"

    #magnets to print
    mag = ["Q1ER_6", "Q2ER_6", "D2ER_6", "Q3ER_6"]
    #mag = ["O3ER_6", "Q3ER_6"]

    #parameters for the magnets
    par = ["B_Field", "B_Gradient", "Entrance_X", "Entrance_Z", "Exit_X", "Exit_Z", "Angle"]
    #par = ["Beta_X", "Beta_Y"]

    inp = open(infile, "r")

    #file header
    head = []
    for i in inp.readline().split("   "):
        if i == "": continue

        head.append(i.strip().replace(" ", "_"))

    #skip the next two lines
    inp.readline()
    inp.readline()

    val = []

    #loop over data lines
    for i in inp:
        ii = i.split()
        lin = []
        for k in range(len(ii)):
            if k < 2:
                lin.append( ii[k] )
            else:
                lin.append( float(ii[k]) )
        val.append(lin)

    df = DataFrame(val, columns=head)
    df.to_csv("lat.csv")

    #magnet loop
    for m in mag:
        for i in range(len(df)):

            if df["Name"][i] == m:
                print(m+":")
                for p in par:
                    print("  "+p+":", df[p][i])


    #for i in range(len(df)):
        #print(df["Name"][i], type(df["Length"][i]))

    #for i in df.iterrows():
    #    print(i["Name"])

    #print(df["Name"])

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    main()
















