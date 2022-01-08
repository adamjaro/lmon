
#ifndef BeamMagnetV2_h
#define BeamMagnetV2_h

// beamline dipole magnet V2

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class GeoParser;

class BeamMagnetV2 : public Detector, public G4VSensitiveDetector {

  public:

    BeamMagnetV2(G4String nam, GeoParser *geo, G4LogicalVolume*);
    virtual ~BeamMagnetV2() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

  private:

    G4String fNam; // magnet name

    void PrintField(G4FieldManager *fman);

    G4VisAttributes* ColorDecoder(GeoParser *geo);

};

#endif

