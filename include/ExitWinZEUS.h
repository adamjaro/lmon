
#ifndef ExitWinZEUS_h
#define ExitWinZEUS_h

// exit window as an Al disc according to ZEUS

#include "globals.hh"
#include "Detector.h"

#include "G4VSensitiveDetector.hh"

class ExitWinZEUS : public Detector, public G4VSensitiveDetector {

  public:

    ExitWinZEUS(): G4VSensitiveDetector(""), fNam(""), fX(0), fY(0), fZ(0) {}
    ExitWinZEUS(const G4String& nam, G4double zpos, G4LogicalVolume*);
    virtual ~ExitWinZEUS() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //getters
    Double_t GetX() const {return fX;}
    Double_t GetY() const {return fY;}
    Double_t GetZ() const {return fZ;}

  private:

    G4String fNam; //! detector name
    Detector *fAddr; //! address of current object

    Double_t fX; // x position of the photon
    Double_t fY; // y position of the photon
    Double_t fZ; // z position of the photon

    //ClassDef(ExitWinZEUS, 1);
};

#endif

