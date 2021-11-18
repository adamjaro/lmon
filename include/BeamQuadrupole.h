
#ifndef BeamQuadrupole_h
#define BeamQuadrupole_h

//beam quadrupole magnet

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class BeamQuadrupole : public Detector, public G4VSensitiveDetector {

  public:

    BeamQuadrupole(G4String nam, GeoParser *geo, G4LogicalVolume*);
    virtual ~BeamQuadrupole() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

  private:

    G4String fNam; // compoment name

    G4bool fRemoveTracks; // stop and remove tracks incident on magnet vessel if set to true

    void PrintField(G4FieldManager *fman);




};

#endif

