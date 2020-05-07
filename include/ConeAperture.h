
#ifndef ConeAperture_h
#define ConeAperture_h

//conical aperture which absorbs all particles hitting its volume

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class ConeAperture : public Detector, public G4VSensitiveDetector {

  public:

    ConeAperture(G4String nam, GeoParser *geo, G4LogicalVolume*);
    virtual ~ConeAperture() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

  private:

    G4String fNam; // compoment name

    G4bool fIsTransparent; // transparency for particles




};

#endif

