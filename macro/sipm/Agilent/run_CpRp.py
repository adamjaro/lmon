#!/usr/bin/python3

#from ctypes import c_double

import code
import readline

from E4980A import E4980A

#_____________________________________________________________________________
def main():

    #LCR meter
    lc = E4980A("192.168.1.101", 5024)

    #lc.run()
    #lc.ramp_down()

    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    main()
























