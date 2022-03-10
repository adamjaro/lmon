
#ifndef MCEvent_h
#define MCEvent_h

#include "Detector.h"
#include "Rtypes.h"

#include "MCEvtDat.h"

class MCEvent : public Detector {

  public:

    MCEvent();
    virtual ~MCEvent() {}

    void BeginEvent(const G4Event *evt);

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

  private:

    void ReadEvtDat(const G4Event *evt);

    G4String fNam; // class name

    MCEvtDat fDat; //event data

    // MC generated particles
    std::vector<Int_t> fPartPdg; //particle pdg
    std::vector<Float_t> fPartPx; //particle px, GeV
    std::vector<Float_t> fPartPy; //particle py, GeV
    std::vector<Float_t> fPartPz; //particle pz, GeV
    std::vector<Float_t> fPartEn; //particle energy, GeV
    std::vector<Float_t> fPartVx; //particle position in x, mm
    std::vector<Float_t> fPartVy; //particle position in y, mm
    std::vector<Float_t> fPartVz; //particle position in z, mm

};

#endif

