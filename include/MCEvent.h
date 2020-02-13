
#ifndef MCEvent_h
#define MCEvent_h

#include "Detector.h"
#include "Rtypes.h"

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

    void ReadPhoton(G4PrimaryParticle *part);
    void ReadElectron(G4PrimaryParticle *part);
    void GetThetaPhi(G4PrimaryParticle *part, Double_t &theta, Double_t &phi);

    G4String fNam; // class name

    Double_t fPhotGen; // energy of generated photon
    Double_t fPhotTheta; // polar angle of generated photon
    Double_t fPhotPhi; // azimuthan angle  of generated photon

    Double_t fVx; // x of generated vertex, mm
    Double_t fVy; // y of generated vertex, mm
    Double_t fVz; // z of generated vertex, mm

    Double_t fElGen; // energy of scattered electron
    Double_t fElTheta; // polar angle of generated photon
    Double_t fElPhi; // azimuthan angle  of generated photon

};

#endif

