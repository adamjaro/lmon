#!/usr/bin/python3

#from ctypes import c_double

import code
import readline

from E4980A import E4980A

#_____________________________________________________________________________
def main():

    #LCR meter
    lc = E4980A("192.168.1.101", 5024)

    #start the interactive shell, call 'lc.configure()' to set for Cp-Rp
    #and 'lc.run()' to make the measurement

    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    main()
























