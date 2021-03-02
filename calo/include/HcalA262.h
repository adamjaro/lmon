
#ifndef HcalA262_h
#define HcalA262_h

// NIM A262 (1987) 229-242

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class GeoParser;

class HcalA262 : public Detector, public G4VSensitiveDetector {

  public:

    HcalA262(const G4String&, GeoParser*, G4LogicalVolume *top);
    virtual ~HcalA262() {}

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //called via Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; // name of detector sensitive logical volume


















};

#endif

