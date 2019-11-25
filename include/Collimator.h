
#ifndef Collimator_h
#define Collimator_h

// collimator between photon exit window and dipole magnet

class Collimator {

  public:

    Collimator(G4double zpos, G4LogicalVolume*);
    virtual ~Collimator() {}

};

#endif

