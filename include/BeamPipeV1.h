
#ifndef BeamPipeV1_h
#define BeamPipeV1_h

//beam pipe element for particle counts on its inner wall

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class BeamPipeV1 : public Detector, public G4VSensitiveDetector {

  public:

    BeamPipeV1(G4String nam, GeoParser *geo, G4LogicalVolume*);
    virtual ~BeamPipeV1() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory*);

  private:

    G4String fNam; // compoment name

    //hits array
    std::vector<Int_t> fHitPdg; // particle pdg
    std::vector<Float_t> fHitEn; // hit energy, GeV
    std::vector<Float_t> fHitX; // hit position in x, mm
    std::vector<Float_t> fHitY; // hit position in y, mm
    std::vector<Float_t> fHitZ; // hit position in z, mm

};

#endif



