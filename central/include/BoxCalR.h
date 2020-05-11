
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
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

  private:

    G4String fNam; // detector name

    Bool_t fIsHit; // hit in event
    Double_t fEnAll; // sum of energy of all particles in event, GeV

    Double_t fHx; // first hit by primary particle in x, mm
    Double_t fHy; // first hit by primary particle in y, mm
    Double_t fHz; // first hit by primary particle in z, mm

    //hits array
    std::vector<Int_t> fHitPdg; // particle pdg
    std::vector<Float_t> fHitEn; // hit energy, GeV
    std::vector<Float_t> fHitX; // hit position in x, mm
    std::vector<Float_t> fHitY; // hit position in y, mm
    std::vector<Float_t> fHitZ; // hit position in z, mm

    G4bool fPrimHit; // flag for hit by primary particle

};

#endif

