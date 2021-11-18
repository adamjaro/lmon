
from ctypes import c_double

import ROOT as rt

from segment import segment

#_____________________________________________________________________________
class magnet(segment):
    #_____________________________________________________________________________
    def __init__(self, nam, geo):

        inner_r = c_double(0)
        geo.GetOptD(nam, "inner_r", inner_r) # mm
        geo.GetOptD(nam, "r1", inner_r) # mm

        self.dx = 2.*inner_r.value
        self.dy = 2.*inner_r.value

        length = c_double(0)
        geo.GetOptD(nam, "length", length) # mm
        geo.GetOptD(nam, "dz", length) # mm

        self.dz = length.value

        xpos = c_double(0)
        geo.GetOptD(nam, "xpos", xpos) # mm
        self.xpos = xpos.value
        self.zpos = geo.GetD(nam, "zpos") # mm

        theta = c_double(0)
        geo.GetOptD(nam, "theta", theta) # rad
        self.theta = theta.value

        self.fill_style = 1000
        self.line_col = rt.kAzure
        self.fill_col = rt.kOrange
        self.line_width = 2

        self.label = ""

        #draw as projection in x or y
        self.y_project = False















