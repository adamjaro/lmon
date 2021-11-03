#!/usr/bin/python3

from math import *

#_____________________________________________________________________________
def main():

    B2BeR_End_Z = -14865.
    B2BeR_InnerRadius = 98.

    B2BeR_Z = B2BeR_End_Z
    B2BeR_XB = -B2BeR_InnerRadius

    Q3eR_ZB = Q3eR_StartZ+Q3eR_InnerRadius*sin(Q3eR_Theta)
    Q3eR_XB = Q3eR_StartX-Q3eR_InnerRadius*cos(Q3eR_Theta)

    print("Q3eR_ZB:", Q3eR_ZB)
    print("Q3eR_XB:", Q3eR_XB)

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    main()

