
#ifndef PolTrackLay_h
#define PolTrackLay_h

// simple tracking layer

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class G4VPhysicalVolume;
class G4Step;
class GeoParser;

class PolTrackLay : public Detector, public G4VSensitiveDetector {

  public:

    PolTrackLay(const G4String&, GeoParser *geo, G4LogicalVolume *top);
    virtual ~PolTrackLay() {}

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

  private:

    G4String fNam; // detector name

    G4VisAttributes *ColorDecoder(GeoParser *geo);

    //hits array
    std::vector<Int_t> fHitPdg; // particle pdg
    std::vector<Float_t> fHitEtrack; // track energy in hit, GeV
    std::vector<Float_t> fHitEdep; // deposited energy in hit, GeV
    std::vector<Float_t> fHitX; // hit position in x, mm
    std::vector<Float_t> fHitY; // hit position in y, mm
    std::vector<Float_t> fHitZ; // hit position in z, mm
    std::vector<Float_t> fHitStepL; // step length in hit, mm
    std::vector<Float_t> fHitTime; // hit time, ns

};

#endif



















