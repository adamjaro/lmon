
#ifndef Magnet_h
#define Magnet_h

// spectrometer dipole magnet

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class GeoParser;

class Magnet : public Detector, public G4VSensitiveDetector {

  public:

    Magnet(const G4String&, GeoParser *geo, G4LogicalVolume*);
    virtual ~Magnet() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step*, G4TouchableHistory*);

  private:

    G4String fNam; // compoment name

    G4bool fRemoveTracks; // stop and remove tracks incident on magnet vessel if set to true

};

#endif

