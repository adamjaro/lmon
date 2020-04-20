
#ifndef BoxCalV2_h
#define BoxCalV2_h

// simple calorimeter, V2

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class G4VPhysicalVolume;
class G4Step;
class GeoParser;

class BoxCalV2 : public Detector, public G4VSensitiveDetector {

  public:

    BoxCalV2(const G4String&, GeoParser *geo, G4LogicalVolume *top);
    virtual ~BoxCalV2() {}

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //called via Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

  private:

    G4String fNam; // detector name

    Bool_t fIsHit; // hit by primary particle
    Double_t fEn; // energy of the primary particle

    Double_t fHx; // hit position in x
    Double_t fHy; // hit position in y
    Double_t fHz; // hit position in z

/*
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
*/
};

#endif



















