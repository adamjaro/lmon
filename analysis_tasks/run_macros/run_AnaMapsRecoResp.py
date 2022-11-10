#!/usr/bin/python3

import sys
from ctypes import CDLL, c_char_p

#_____________________________________________________________________________
def get_config():

    #command line options
    args = sys.argv
    if len(args) < 2:
        print("No configuration specified.")
        quit()
    args.pop(0)

    return args.pop(0)

#get_config

#_____________________________________________________________________________
if __name__ == "__main__":

    #load the analysis library and run the task
    CDLL("liblmonAnalysisTasks.so").make_AnaMapsRecoResp(c_char_p(bytes(get_config(), "utf-8")))



