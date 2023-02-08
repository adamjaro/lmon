
#ifndef TrackingAction_h
#define TrackingAction_h

#include<unordered_map>

#include "Rtypes.h"

#include "G4UserTrackingAction.hh"

class TTree;

class TrackingAction : public G4UserTrackingAction {

  public:

    TrackingAction();

    void PreUserTrackingAction(const G4Track *) override;

    void Reset() const;

    G4int GetPrimaryID(G4int id) const;

    void CreateOutput(TTree *tree) const;

  private:

    std::unordered_map<G4int, G4int> *fStack; // local stack for primary particle IDs

    void AddMCParticle(const G4Track*);

    //output on MC particles
    std::vector<Int_t> *fMCPdg; // particle pdg
    std::vector<Int_t> *fMCItrk; // track ID for the particle
    std::vector<Double_t> *fMCEn; // particle energy, GeV
    std::vector<Double_t> *fMCTheta; // particle polar angle, rad
    std::vector<Double_t> *fMCPhi; // particle azimuthal angle, rad
    std::vector<Double_t> *fMCVx; // particle vertex position in x, mm
    std::vector<Double_t> *fMCVy; // particle vertex position in x, mm
    std::vector<Double_t> *fMCVz; // particle vertex position in x, mm

};

#endif

