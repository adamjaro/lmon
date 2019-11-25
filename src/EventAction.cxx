
//_____________________________________________________________________________
//
// standard event action,
// calls ClearEvent and FinishEvent in DetectorConstruction
//_____________________________________________________________________________

//Geant headers
#include "G4Event.hh"
#include "G4RunManager.hh"

//local headers
#include "EventAction.h"
#include "DetectorConstruction.h"

//_____________________________________________________________________________
EventAction::EventAction() : G4UserEventAction(), fDet(0) {

  //get the detector
  fDet = static_cast<const DetectorConstruction*>( G4RunManager::GetRunManager()->GetUserDetectorConstruction() );

}//EventAction

//_____________________________________________________________________________
void EventAction::BeginOfEventAction(const G4Event *) {

  //clear the detectors
  fDet->ClearEvent();

}//BeginOfEventAction

//_____________________________________________________________________________
void EventAction::EndOfEventAction(const G4Event *evt) {

  //write detector event output
  fDet->FinishEvent(evt);

}//EndOfEventAction














