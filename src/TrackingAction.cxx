
//ROOT
#include "TTree.h"

//Geant
#include "G4Track.hh"
#include "G4SystemOfUnits.hh"

//local classes
#include "TrackingAction.h"

using namespace std;

//_____________________________________________________________________________
TrackingAction::TrackingAction() : G4UserTrackingAction() {

  G4cout << "TrackingAction::TrackingAction " << this << G4endl;

  //create the local stack
  fStack = new unordered_map<G4int, G4int>;

  //output on MC particles
  fMCPdg = new vector<Int_t>;
  fMCItrk = new vector<Int_t>;
  fMCEn = new vector<Double_t>;
  fMCTheta = new vector<Double_t>;
  fMCPhi = new vector<Double_t>;
  fMCVx = new vector<Double_t>;
  fMCVy = new vector<Double_t>;
  fMCVz = new vector<Double_t>;

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
    AddMCParticle(track);
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

  //clear the MC particles
  fMCPdg->clear();
  fMCItrk->clear();
  fMCEn->clear();
  fMCTheta->clear();
  fMCPhi->clear();
  fMCVx->clear();
  fMCVy->clear();
  fMCVz->clear();

}//Reset

//_____________________________________________________________________________
void TrackingAction::CreateOutput(TTree *tree) const {

  //output on MC particles

  tree->Branch("mcp_pdg", fMCPdg);
  tree->Branch("mcp_itrk", fMCItrk);
  tree->Branch("mcp_en", fMCEn);
  tree->Branch("mcp_theta", fMCTheta);
  tree->Branch("mcp_phi", fMCPhi);
  tree->Branch("mcp_vx", fMCVx);
  tree->Branch("mcp_vy", fMCVy);
  tree->Branch("mcp_vz", fMCVz);

}//CreateOutput

//_____________________________________________________________________________
void TrackingAction::AddMCParticle(const G4Track *track) {

  //add MC particle from the track

  //particle kinematics
  const G4DynamicParticle *part = track->GetDynamicParticle();

  //vertex position
  G4ThreeVector vtx = track->GetVertexPosition();

  fMCPdg->push_back( part->GetPDGcode() );
  fMCItrk->push_back( track->GetTrackID() );
  fMCEn->push_back( part->Get4Momentum().e()/GeV );
  fMCTheta->push_back( part->Get4Momentum().theta()/rad );
  fMCPhi->push_back( part->Get4Momentum().phi()/rad );
  fMCVx->push_back( vtx.x()/mm );
  fMCVy->push_back( vtx.y()/mm );
  fMCVz->push_back( vtx.z()/mm );

}//AddMCParticle



































