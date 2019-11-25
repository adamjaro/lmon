
#ifndef EventAction_h
#define EventAction_h

// standard event action

#include "G4UserEventAction.hh"

class DetectorConstruction;

class EventAction : public G4UserEventAction {

  public:

    EventAction();
    virtual ~EventAction() {}

    virtual void BeginOfEventAction(const G4Event*);
    virtual void EndOfEventAction(const G4Event*);

  private:

    const DetectorConstruction *fDet; // detector

};

#endif

