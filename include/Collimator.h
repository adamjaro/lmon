
#ifndef Collimator_h
#define Collimator_h

// collimator between photon exit window and dipole magnet

class GeoParser;

class Collimator {

  public:

    Collimator(const G4String&, GeoParser *geo, G4LogicalVolume*);
    virtual ~Collimator() {}

  private:

    G4String fNam; // component name

};

#endif

