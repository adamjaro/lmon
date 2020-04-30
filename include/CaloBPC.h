
#ifndef CaloBPC_h
#define CaloBPC_h

// tungsten/scintillator calorimeter following the ZEUS BPC

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class GeoParser;

class CaloBPC : public Detector, public G4VSensitiveDetector {

  public:

    CaloBPC(const G4String&, GeoParser *, G4LogicalVolume*);
    virtual ~CaloBPC() {}

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //called via Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *);
    virtual void ClearEvent();
    virtual void FinishEvent();

  private:

    G4String fNam; // name of detector sensitive logical volume
    G4int fNscin; // number of scintillator strips on the layer

    //signal in a given scintillator
    struct ScinSig {
      G4int fIstrip; // strip index on the layer
      G4int fIlay; // layer index in the module
      G4double fEdep; // deposited energy in the scintillator
      ScinSig(G4int istrip, G4int ilay): fIstrip(istrip), fIlay(ilay), fEdep(0) {}
    };
    std::map<G4int, ScinSig> fScinArray; // container for all scintillator signals

    //output on scintillator signals
    std::vector<Int_t> fIstrip; // output strip index
    std::vector<Int_t> fIlay; // output layer index
    std::vector<Float_t> fEdep; // output deposited energy

};

#endif



















