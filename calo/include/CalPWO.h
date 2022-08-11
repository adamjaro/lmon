
#ifndef CalPWO_h
#define CalPWO_h

// PbWO4 calorimeter

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class GeoParser;

class CalPWO : public Detector, public G4VSensitiveDetector {

  public:

    CalPWO(const G4String&, GeoParser*, G4LogicalVolume *top);
    virtual ~CalPWO() {}

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*) { return true; }

    //called via Detector
    virtual const G4String& GetName() const { return fNam; }

  private:

    G4String fNam; // name of detector sensitive logical volume


};

#endif

