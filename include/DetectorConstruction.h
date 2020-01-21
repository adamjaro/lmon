
#ifndef DetectorConstruction_h
#define DetectorConstruction_h

// main detector construction

#include "G4VUserDetectorConstruction.hh"

class G4VPhysicalVolume;
class G4Step;
class G4Event;
class G4GenericMessenger;

#include "Detector.h"

class RootOut;
class vector;
class MCEvent;

class DetectorConstruction : public G4VUserDetectorConstruction {

  public:

    DetectorConstruction();
    virtual ~DetectorConstruction();

    G4VPhysicalVolume* Construct();

    void BeginEvent(const G4Event *evt) const;
    void FinishEvent() const;

    void CreateOutput() const;

    void ConstructSDandField();

  private:

    void AddDetector(Detector *det); // add detector to all detectors

    std::vector<Detector*> *fDet; //all detectors

    RootOut *fOut; // output to ROOT TTree

    MCEvent *fMC; // generated particles

    G4GenericMessenger *fMsg; // messenger for detectors and components
    G4bool fIncCollim; // flag to include the collimator
    G4bool fIncMagnet; // flag for spectrometer magnet
    G4bool fIncEWv2; // flag for photon exit window version 2
    G4bool fIncPhot; // direct photon calorimeter
    G4bool fIncUp; // up spectrometer calorimeter
    G4bool fIncDown; // up spectrometer calorimeter

};

#endif













