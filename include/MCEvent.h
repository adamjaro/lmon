
#ifndef MCEvent_h
#define MCEvent_h

#include "Detector.h"

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

    G4String fNam; // class name

    Double_t fPhotGen; // energy of generated photon
    Double_t fPhotTheta; // polar angle of generated photon
    Double_t fPhotPhi; // azimuthan angle  of generated photon

};

#endif

