
#ifndef TrackingAction_h
#define TrackingAction_h

#include "G4UserTrackingAction.hh"

class TrackingAction : public G4UserTrackingAction {

  public:

    TrackingAction();

    void PreUserTrackingAction(const G4Track *) override;

    void Reset() const;

    G4int GetPrimaryID(G4int id) const;

  private:

    std::unordered_map<G4int, G4int> *fStack; // local stack for primary particle IDs

};

#endif

