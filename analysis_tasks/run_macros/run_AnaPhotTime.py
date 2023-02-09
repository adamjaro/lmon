#!/usr/bin/python3

import sys
from ctypes import CDLL, c_char_p, c_void_p

#_____________________________________________________________________________
def main():

    #configuration from command line
    #config = get_config()
    config = ""

    #analysis library
    lib = CDLL("liblmonAnalysisTasks.so")

    #analysis task
    lib.make_AnaPhotTime.restype = c_void_p
    task = c_void_p(lib.make_AnaPhotTime())

    #run the task    
    lib.run_AnaPhotTime( task, c_char_p(bytes(config, "utf-8")) )

#main

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

    main()

