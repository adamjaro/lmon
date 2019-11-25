
#ifndef DetectorConstruction_h
#define DetectorConstruction_h

// main detector construction

#include "G4VUserDetectorConstruction.hh"

class G4VPhysicalVolume;
class G4Step;
class G4Event;

#include "Detector.h"

class TFile;
class TTree;
class vector;

#include "Rtypes.h"

class DetectorConstruction : public G4VUserDetectorConstruction {

  public:

    DetectorConstruction();
    virtual ~DetectorConstruction();

    G4VPhysicalVolume* Construct();

    void ClearEvent() const;
    void FinishEvent(const G4Event *evt) const;

    void CreateOutput() const;

    void ConstructSDandField();

  private:

    void AddDetector(Detector *det); // add detector to all detectors

    std::vector<Detector*> *fDet; //all detectors

    TFile *fOut; // output file
    TTree *fDetTree; // output tree

    Double_t *fPhotGen; // energy of generated photon, placeholder for a class
                        // holding TClonesArray of TParticles

};

#endif













