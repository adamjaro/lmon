
#ifndef CollimatorV2_h
#define CollimatorV2_h

// collimator between photon exit window and dipole magnet, version 2

class GeoParser;

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class CollimatorV2 : public Detector, public G4VSensitiveDetector {

  public:

    CollimatorV2(const G4String&, GeoParser *geo, G4LogicalVolume*);
    virtual ~CollimatorV2() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

  private:

    G4String fNam; // component name

};

#endif

