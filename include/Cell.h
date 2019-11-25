
#ifndef Cell_h
#define Cell_h

// cell in composite calorimeter

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class CompCal;
class OpDet;

class Cell : public Detector, public G4VSensitiveDetector {

  public:

    Cell(const G4String& nam, G4int ix, G4int iy, G4int ncells, G4double zpos, G4double ypos, G4LogicalVolume *top, CompCal&);
    virtual ~Cell() {}

    //from G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

    //from Detector
    virtual void Add(std::vector<Detector*> *vec);
    virtual const G4String& GetName() const {return fNam;}
    //event and run from Detector
    virtual void ClearEvent();
    virtual void CreateOutput(TTree *tree);

  private:

    G4String fNam; // cell name

    //helper functios for TTree branches
    void AddBranch(const std::string& nam, Double_t *val, TTree *tree);
    void AddBranch(const std::string& nam, ULong64_t *val, TTree *tree);

    Double_t fE; //deposited energy in the cell
    ULong64_t fNphot; // number of optical photons
    ULong64_t fNscin; // scintillation photons
    ULong64_t fNcerenkov; // Cerenkov photons

    G4int fScinType; // scintillation process type
    G4int fScinSubType; // scintillation process subtype
    G4int fCerenkovType; // Cerenkov process type
    G4int fCerenkovSubType; // Cerenkov process subtype

    OpDet *fOpDet; // optical detector attached to the crystal

    CompCal& det; //ref to detector where this cell is included
    friend class CompCal;

};

#endif





















