
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
class GeoParser;

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

    void AddDetector(unsigned int i, G4LogicalVolume *top); // add detector to all detectors

    std::vector<Detector*> *fDet; //all detectors

    RootOut *fOut; // output to ROOT TTree

    MCEvent *fMC; // generated particles

    GeoParser *fGeo; // geometry parser
    G4String fGeoName; // name of geometry input

    G4GenericMessenger *fMsg; // messenger for geometry input

};

#endif













