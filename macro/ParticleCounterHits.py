
# ParticleCounter hits collection

from ROOT import std, TVector3

#_____________________________________________________________________________
class ParticleCounterHits:
    #_____________________________________________________________________________
    def __init__(self, name, tree):

        #hit representation in the tree
        self.pdg = std.vector(int)()
        self.en = std.vector(float)()
        self.hx = std.vector(float)()
        self.hy = std.vector(float)()
        self.hz = std.vector(float)()

        tree.SetBranchAddress(name+"_HitPdg", self.pdg)
        tree.SetBranchAddress(name+"_HitEn", self.en)
        tree.SetBranchAddress(name+"_HitX", self.hx)
        tree.SetBranchAddress(name+"_HitY", self.hy)
        tree.SetBranchAddress(name+"_HitZ", self.hz)

        #interface to the hit
        self.hit = self.Hit()

    #_____________________________________________________________________________
    def GetHit(self, ihit):

        #get the hit at 'ihit'

        self.hit.pdg = self.pdg.at(ihit)
        self.hit.en = self.en.at(ihit)
        self.hit.x = self.hx.at(ihit)
        self.hit.y = self.hy.at(ihit)
        self.hit.z = self.hz.at(ihit)

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

        #_____________________________________________________________________________
        def GlobalToLocal(self, x0, y0, z0, theta=0):

            #local detector coordinates with rotation phi in x-z plane
            pos = TVector3(self.x-x0, self.y-y0, self.z-z0)
            pos.RotateY(-theta)

            self.x = pos.X()
            self.y = pos.Y()
            self.z = pos.Z()

    #_____________________________________________________________________________
    def GetN(self):

        #number of hits in event, all vectors are of same size

        return self.pdg.size()


    #direct access:
    #_____________________________________________________________________________
    def GetPdg(self, ihit):
        return self.pdg.at(ihit)

    #_____________________________________________________________________________
    def GetX(self, ihit):
        return self.hx.at(ihit)

    #_____________________________________________________________________________
    def GetY(self, ihit):
        return self.hy.at(ihit)

    #_____________________________________________________________________________
    def GetZ(self, ihit):
        return self.hz.at(ihit)

    #_____________________________________________________________________________
    def GetEn(self, ihit):
        return self.en.at(ihit)











