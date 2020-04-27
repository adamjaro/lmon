
#ifndef OpDet_h
#define OpDet_h

// detector for optical photons

#include "CLHEP/Random/Random.h"

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class OpHitsArray;

class OpDet : public Detector, public G4VSensitiveDetector {

  public:

    OpDet(const G4String& name, G4double xysiz, G4double zpos, G4double xmid, G4double ymid, G4LogicalVolume *top);
    virtual ~OpDet();

    //G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //Detector
    virtual void Add(std::vector<Detector*> *vec) {vec->push_back(this);}
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();
    virtual void FinishEvent();

    G4VPhysicalVolume *GetPhysicalVolume() const {return fPhys;}

  private:

    void AddBranch(const std::string& nam, Double_t *val, TTree *tree);
    void AddBranch(const std::string& nam, ULong64_t *val, TTree *tree);

    Double_t fEdep; // total energy deposited in optical photon detector
    Double_t fEopt; // energy deposited by optical photons
    ULong64_t fNphot; // number of photons in event
    ULong64_t fNscin; // scintillation photons
    ULong64_t fNcerenkov; // Cerenkov photons

    Double_t fTmin; // time of first detected photon
    Double_t fTmax; // time of last detected photon
    Double_t fTavg; // average time of all detected photons

    G4VPhysicalVolume *fPhys; // optical detector physical volume
    G4String fNam; // detector name

    G4double fQE; // quantum efficiency
    CLHEP::HepRandom *fRand; // random generator for quantum efficiency

    G4int fScinType; // scintillation process type
    G4int fScinSubType; // scintillation process subtype
    G4int fCerenkovType; // Cerenkov process type
    G4int fCerenkovSubType; // Cerenkov process subtype

    OpHitsArray *fHits; // hits array for the detector

    friend class CompCal;

};

#endif

