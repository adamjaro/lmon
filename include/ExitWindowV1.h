
#ifndef ExitWindowV1_h
#define ExitWindowV1_h

// Exit window version 1

#include "globals.hh"
#include "Detector.h"

#include "G4VSensitiveDetector.hh"

class GeoParser;

class ExitWindowV1 : public Detector, public G4VSensitiveDetector {

  public:

    ExitWindowV1(const G4String& nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

  private:

    G4LogicalVolume* GetMotherVolume(G4String mother_nam, G4LogicalVolume *top);

    G4String fNam; // detector name

    //hits array
    std::vector<Int_t> fHitPdg; // particle pdg
    std::vector<Float_t> fHitEn; // particle energy, GeV
    std::vector<Float_t> fHitX; // hit position in x, mm
    std::vector<Float_t> fHitY; // hit position in y, mm
    std::vector<Float_t> fHitZ; // hit position in z, mm
    std::vector<Int_t> fHitPrim; // primary particle, bool
    std::vector<Int_t> fHitConv; // conversion in the hit, bool
    std::vector<Float_t> fHitEdep; // deposited energy in hit, GeV
    std::vector<Int_t> fHitNsec; // number of secondaries in hit

};

#endif














