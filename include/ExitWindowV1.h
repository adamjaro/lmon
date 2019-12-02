
#ifndef ExitWindowV1_h
#define ExitWindowV1_h

// Exit window version 1

#include "globals.hh"
#include "Detector.h"

#include "G4VSensitiveDetector.hh"

class ExitWindowV1 : public Detector, public G4VSensitiveDetector {

  public:

    enum geom {kFlat, kTilt}; // geometry selection

    ExitWindowV1(const G4String& nam, G4double zpos, geom geo, G4LogicalVolume*);
    virtual ~ExitWindowV1() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();
    virtual void FinishEvent();

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

  private:

    G4String fNam; // detector name
    G4double fZpos; // position of the exit window along z
    G4Material *fMat; // material for the exit window
    G4LogicalVolume *fTop; // to volume to place the exit window

    void ConstructFlat();
    void ConstructTilt();

    Double_t fPhotX; // x position of the photon
    Double_t fPhotY; // y position of the photon
    Double_t fPhotZ; // z position of the photon

    Bool_t fConv; // flag set when e+e- conversion took place
    Bool_t fMuConv; // flag for mu+mu- conversion

    Double_t fConvX; // x of conversion point
    Double_t fConvY; // y of conversion point
    Double_t fConvZ; // z of conversion point

    Double_t fConvStepLen; // length of step with conversion
    Double_t fPhotConvLen; // length between photon first point and conversion point

};

#endif














