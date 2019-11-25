
#ifndef BoxCal_h
#define BoxCal_h

// simple calorimeter

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class G4VPhysicalVolume;
class G4Step;

class OpDet;

class BoxCal : public Detector, public G4VSensitiveDetector {

  public:

    BoxCal(const G4String&, G4double zpos, G4double ypos, G4LogicalVolume*);
    virtual ~BoxCal() {}

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //called via Detector
    virtual void Add(std::vector<Detector*> *vec);
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

  private:

    G4String fNam; // detector name
    G4VPhysicalVolume *fSens; //detector sensitive volume
    OpDet *fOpDet; // optical detector attached to the crystal

    void AddBranch(const std::string& nam, Double_t *val, TTree *tree);
    void AddBranch(const std::string& nam, ULong64_t *val, TTree *tree);

    Double_t fEdep; // deposited energy in the detector
    Double_t fX; // x of first point in the detector
    Double_t fY; // y of first point
    Double_t fZ; // z of first point

    ULong64_t fNphot; // number of optical photons
    ULong64_t fNscin; // scintillation photons
    ULong64_t fNcerenkov; // Cerenkov photons

    G4int fScinType; // scintillation process type
    G4int fScinSubType; // scintillation process subtype
    G4int fCerenkovType; // Cerenkov process type
    G4int fCerenkovSubType; // Cerenkov process subtype

};

#endif



















