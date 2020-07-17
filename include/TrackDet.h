
#ifndef TrackDet_h
#define TrackDet_h

// simple tracking layer

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class G4VPhysicalVolume;
class G4Step;
class GeoParser;

class TrackDet : public Detector, public G4VSensitiveDetector {

  public:

    TrackDet(const G4String&, GeoParser *geo, G4LogicalVolume *top);
    virtual ~TrackDet() {}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

  private:

    G4String fNam; // detector name

    Bool_t fIsHit; // hit in event
    Double_t fEnAll; // sum of energy of all particles in event, GeV

    //hits array
    std::vector<Int_t> fHitPdg; // particle pdg
    std::vector<Float_t> fHitEn; // hit energy, GeV
    std::vector<Float_t> fHitX; // hit position in x, mm
    std::vector<Float_t> fHitY; // hit position in y, mm
    std::vector<Float_t> fHitZ; // hit position in z, mm

};

#endif



















