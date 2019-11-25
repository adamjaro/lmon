
#ifndef CompCal_h
#define CompCal_h

// composite calorimeter

#include "Detector.h"

class Cell;

class CompCal : public Detector {

  public:

    CompCal(const G4String&, G4double zpos, G4double ypos, G4LogicalVolume*);
    virtual ~CompCal() {}

    virtual void Add(std::vector<Detector*> *vec);
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();
    virtual void FinishEvent();

  private:

    G4String fNam; // detector name

    void AddBranch(const std::string& nam, Double_t *val, TTree *tree);
    void AddBranch(const std::string& nam, ULong64_t *val, TTree *tree);

    Double_t fEdep; // deposited energy in the detector
    Double_t fX; // x of first point in the detector
    Double_t fY; // y of first point
    Double_t fZ; // z of first point
    Double_t fXyzE; // track energy at the first point

    ULong64_t fNphot; // number of optical photons from all cells
    ULong64_t fNscin; // scintillation photons from all cells
    ULong64_t fNcerenkov; // Cerenkov photons from all cells

    ULong64_t fNphotDet; // detected optical photons from cell photon detectors
    ULong64_t fNscinDet; // detected scintillation photons from all cell photon detectors
    ULong64_t fNcerenkovDet; // detected Cerenkov photons from all cells photon detectors

    std::vector<Cell*> *fCells; //detector cells

    friend class Cell;

};

#endif

