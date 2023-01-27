
//C++
#include<unordered_map>

//Geant
#include "G4Track.hh"

//local classes
#include "TrackingAction.h"

using namespace std;

//_____________________________________________________________________________
TrackingAction::TrackingAction() : G4UserTrackingAction() {

  G4cout << "TrackingAction::TrackingAction " << this << G4endl;

  //create the local stack
  fStack = new unordered_map<G4int, G4int>;

}//TrackingAction

//_____________________________________________________________________________
void TrackingAction::PreUserTrackingAction(const G4Track *track) {

  //current track ID
  G4int trackID = track->GetTrackID();

  //track already seen
  if( fStack->find(trackID) != fStack->end() ) return;

  //parent ID for current track
  G4int parentID = track->GetParentID();

  //G4cout << "TrackingAction::PreUserTrackingAction, track ID: " << trackID << " " << parentID << G4endl;

  //primary track, add the track ID as mapped value
  if( parentID == 0 ) {

    fStack->emplace(trackID, trackID);
    return;
  }

  //secondary track, assign its primary ID as mapped value
  fStack->emplace(trackID, fStack->at(parentID));

  //G4cout << "TrackingAction::PreUserTrackingAction, prim ID:  " << fStack->at(trackID) << G4endl;

}//PreUserTrackingAction

//_____________________________________________________________________________
G4int TrackingAction::GetPrimaryID(G4int id) const {

  //retrieve ID of primary particle belonging to a track at id in the argument

  return fStack->at(id);

}//GetPrimaryID

//_____________________________________________________________________________
void TrackingAction::Reset() const {

  //G4cout << "TrackingAction::Reset " << this << G4endl;

  //remove all particles
  fStack->clear();

}//Reset
















