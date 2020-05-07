
#ifndef BoxCalR_h
#define BoxCalR_h

//testing calorimeter with radial symmetry

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class GeoParser;

class BoxCalR : public Detector, public G4VSensitiveDetector {

  public:

    BoxCalR(G4String nam, GeoParser *geo, G4LogicalVolume*);
    virtual ~BoxCalR() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

  private:

    G4String fNam; // detector name

};

#endif

