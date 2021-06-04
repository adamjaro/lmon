
# ExitWindowV1 hits

from ctypes import c_bool

from ROOT import std, TVector3

#_____________________________________________________________________________
class ew_hits:
    #_____________________________________________________________________________
    def __init__(self, name, tree):

        #hit representation in the tree
        self.pdg = std.vector(int)()
        self.en = std.vector(float)()
        self.hx = std.vector(float)()
        self.hy = std.vector(float)()
        self.hz = std.vector(float)()
        self.prim = std.vector(int)()
        self.conv = std.vector(int)()
        self.edep = std.vector(float)()
        self.nsec = std.vector(int)()

        tree.SetBranchAddress(name+"_HitPdg", self.pdg)
        tree.SetBranchAddress(name+"_HitEn", self.en)
        tree.SetBranchAddress(name+"_HitX", self.hx)
        tree.SetBranchAddress(name+"_HitY", self.hy)
        tree.SetBranchAddress(name+"_HitZ", self.hz)
        tree.SetBranchAddress(name+"_HitPrim", self.prim)
        tree.SetBranchAddress(name+"_HitConv", self.conv)
        tree.SetBranchAddress(name+"_HitEdep", self.edep)
        tree.SetBranchAddress(name+"_HitNsec", self.nsec)

        #interface to the hit
        self.hit = self.Hit()

    #_____________________________________________________________________________
    def get_hit(self, ihit):

        #get the hit at 'ihit'

        self.hit.pdg = self.pdg.at(ihit)
        self.hit.en = self.en.at(ihit)
        self.hit.x = self.hx.at(ihit)
        self.hit.y = self.hy.at(ihit)
        self.hit.z = self.hz.at(ihit)
        self.hit.prim = self.prim.at(ihit)
        self.hit.conv = self.conv.at(ihit)
        self.hit.edep = self.edep.at(ihit)
        self.hit.nsec = self.nsec.at(ihit)

        return self.hit

    #_____________________________________________________________________________
    class Hit:
        #implementation for the hit interface
        #_____________________________________________________________________________
        def __init__(self):
            self.pdg = 0 # PDG
            self.en = 0. # GeV
            self.x = 0. # mm
            self.y = 0. # mm
            self.z = 0. # mm
            self.prim = False # bool
            self.conv = False # bool
            self.edep = 0. # GeV
            self.nsec = 0 # int

        #_____________________________________________________________________________
        def global_to_zpos(self, z0):

            #coordinates at z position of the exit window
            pos = TVector3(self.x, self.y, self.z-z0)

            self.x = pos.X()
            self.y = pos.Y()
            self.z = pos.Z()

    #_____________________________________________________________________________
    def get_n(self):

        #number of hits in event, all vectors are of same size

        return self.pdg.size()

