
#ifndef WScFiZX_h
#define WScFiZX_h

// W/ScFi by Zhiwan Xu (UCLA)

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class GeoParser;

class WScFiZX : public Detector, public G4VSensitiveDetector {

  public:

    WScFiZX(const G4String&, GeoParser*, G4LogicalVolume *top);
    virtual ~WScFiZX() {}

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

    //called via Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void ClearEvent();
    virtual void CreateOutput(TTree *tree);

  private:

    G4double BirksCorrectedEnergyDeposit(G4Step *step);

    G4String fNam; // name of detector sensitive logical volume
    G4double fBirksCoefficient; // value of Birks coefficient in mm/MeV

    G4bool fCheckOverlaps; // option to activate checking of volumes overlaps

    Double_t fEdep; // deposited energy, GeV

};

#endif

