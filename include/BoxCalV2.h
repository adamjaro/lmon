
#ifndef BoxCalV2_h
#define BoxCalV2_h

// simple calorimeter, V2

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class G4VPhysicalVolume;
class G4Step;
class GeoParser;

class BoxCalV2 : public Detector, public G4VSensitiveDetector {

  public:

    BoxCalV2(const G4String&, GeoParser *geo, G4LogicalVolume *top);
    virtual ~BoxCalV2() {}

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //called via Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

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



















