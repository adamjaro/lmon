
//_____________________________________________________________________________
//
// Hits for TrkMapsBasic
//
//_____________________________________________________________________________

//C++
#include <map>
#include <vector>

//ROOT
#include "TTree.h"
#include "TVector3.h"

//Geant
#include "G4SystemOfUnits.hh"
#include "G4RunManager.hh"

//local classes
#include "DetUtils.h"
#include "GeoParser.h"
#include "TrackingAction.h"
#include "TrkMapsBasicHits.h"

using namespace std;

//_____________________________________________________________________________
TrkMapsBasicHits::TrkMapsBasicHits(): fStack(0), fXpos(0), fYpos(0), fZpos(0), fThetaX(0), fThetaY(0) {

}//ParticleCounterHits

//_____________________________________________________________________________
void TrkMapsBasicHits::AddSignal(G4int ipix, G4int irow, G4double x, G4double y, G4double z, G4double en,
    G4int itrk, G4int pdg, G4bool is_prim) {

  //add signal for a given pixel

  //hit at a given pixel location given by ipix and irow
  map<pair<Int_t, Int_t>, Hit>::iterator it = fHitsW.find( pair(ipix, irow) );

  //ID of primary particle for the hit
  Int_t prim_id = fStack->GetPrimaryID(itrk);

  //create new hit at a given location if not alread present
  if( it == fHitsW.end() ) {

    it = fHitsW.insert( make_pair(pair(ipix, irow), Hit(ipix, irow, x, y, z, itrk, pdg, is_prim, prim_id)) ).first;
  }

  //add deposited energy in the hit
  Hit& hit = (*it).second;
  hit.en += en;

  //lowest track ID associated with the hit and its PDG code
  if( itrk < hit.itrk ) {
    hit.itrk = itrk;
    hit.pdg = pdg;
  }

  //update primary flag if not set
  if( hit.is_prim == kFALSE ) {
    hit.is_prim = is_prim;
  }

  //lowest primary ID for the hit
  if( prim_id < hit.prim_id ) {

    hit.prim_id = prim_id;
  }

  //G4cout << "TrkMapsBasicHits::AddSignal " << itrk << " " << fStack->GetPrimaryID(itrk) << G4endl; 

}//AddSignal

//_____________________________________________________________________________
void TrkMapsBasicHits::CreateOutput(G4String nam, TTree *tree) {

  //output from TrkMapsBasicHits

  fIpix = new vector<Int_t>();
  fIrow = new vector<Int_t>();
  fX = new vector<Double_t>();
  fY = new vector<Double_t>();
  fZ = new vector<Double_t>();
  fEn = new vector<Double_t>();
  fItrk = new vector<Int_t>();
  fPdg = new vector<Int_t>();
  fPrim = new vector<Bool_t>();
  fPrimID = new vector<Int_t>();

  DetUtils u(nam, tree);

  u.AddBranch("_HitIpix", fIpix);
  u.AddBranch("_HitIrow", fIrow);

  u.AddBranch("_HitX", fX);
  u.AddBranch("_HitY", fY);
  u.AddBranch("_HitZ", fZ);
  u.AddBranch("_HitEn", fEn);

  u.AddBranch("_HitItrk", fItrk);
  u.AddBranch("_HitPdg", fPdg);
  u.AddBranch("_HitPrim", fPrim);
  u.AddBranch("_HitPrimID", fPrimID);

  //load the tracking action for primary particle IDs
  fStack = static_cast<const TrackingAction*>( G4RunManager::GetRunManager()->GetUserTrackingAction() );

}//CreateOutput

//_____________________________________________________________________________
void TrkMapsBasicHits::ClearEvent() {

  //clear hit structures at the beginning of the event

  fHitsW.clear();

  fIpix->clear();
  fIrow->clear();
  fX->clear();
  fY->clear();
  fZ->clear();
  fEn->clear();
  fItrk->clear();
  fPdg->clear();
  fPrim->clear();
  fPrimID->clear();

  //G4cout << "TrkMapsBasicHits::ClearEvent" << G4endl;

}//ClearEvent

//_____________________________________________________________________________
void TrkMapsBasicHits::FinishEvent() {

  //write hits to the output

  //hits loop
  for(map<pair<Int_t, Int_t>, Hit>::iterator i = fHitsW.begin(); i != fHitsW.end(); i++) {

    const Hit& hit = (*i).second;

    fIpix->push_back( hit.ipix );
    fIrow->push_back( hit.irow );

    fX->push_back( hit.x );
    fY->push_back( hit.y );
    fZ->push_back( hit.z );
    fEn->push_back( hit.en );

    fItrk->push_back( hit.itrk );
    fPdg->push_back( hit.pdg );
    fPrim->push_back( hit.is_prim );
    fPrimID->push_back( hit.prim_id );

    //G4cout << hit.itrk << " " << hit.pdg <<  " " << hit.ipix << " " << hit.irow << " " << hit.en;
    //G4cout << " " << hit.x << " " << hit.y << " " << hit.z << " " << hit.is_prim << " " << hit.prim_id << G4endl;

  }//hits loop

}//FinishEvent

//_____________________________________________________________________________
void TrkMapsBasicHits::ConnectInput(std::string nam, TTree *tree) {

  //connect hits from input tree

  fIpix = 0x0;
  fIrow = 0x0;
  fX = 0x0;
  fY = 0x0;
  fZ = 0x0;
  fEn = 0x0;
  fItrk = 0x0;
  fPdg = 0x0;
  fPrim = 0x0;
  fPrimID = 0x0;

  tree->SetBranchAddress((nam+"_HitIpix").c_str(), &fIpix);
  tree->SetBranchAddress((nam+"_HitIrow").c_str(), &fIrow);

  tree->SetBranchAddress((nam+"_HitX").c_str(), &fX);
  tree->SetBranchAddress((nam+"_HitY").c_str(), &fY);
  tree->SetBranchAddress((nam+"_HitZ").c_str(), &fZ);
  tree->SetBranchAddress((nam+"_HitEn").c_str(), &fEn);

  tree->SetBranchAddress((nam+"_HitItrk").c_str(), &fItrk);
  tree->SetBranchAddress((nam+"_HitPdg").c_str(), &fPdg);
  tree->SetBranchAddress((nam+"_HitPrim").c_str(), &fPrim);

  if( tree->FindBranch((nam+"_HitPrimID").c_str()) ) {
    tree->SetBranchAddress((nam+"_HitPrimID").c_str(), &fPrimID);
  }

}//ConnectInput

//_____________________________________________________________________________
void TrkMapsBasicHits::LoadHits() {

  //load hits for a given event

  fHitsR.clear();

  //input vector loop
  for(unsigned long i=0; i<fIpix->size(); i++) {

    Int_t prim_id = 0;
    if(fPrimID) prim_id = fPrimID->at(i);

    fHitsR.push_back( Hit(fIpix->at(i), fIrow->at(i), fX->at(i), fY->at(i), fZ->at(i),
      fItrk->at(i), fPdg->at(i), fPrim->at(i), prim_id) );
    fHitsR.back().en = fEn->at(i);

  }//input vector loop

}//LoadHits

//_____________________________________________________________________________
void TrkMapsBasicHits::LocalFromGeo(G4String nam, GeoParser *geo) {

  //plane position from geometry

  geo->GetOptD(nam, "xpos", fXpos, GeoParser::Unit(mm));
  geo->GetOptD(nam, "ypos", fYpos, GeoParser::Unit(mm));
  geo->GetOptD(nam, "zpos", fZpos, GeoParser::Unit(mm));

  G4double theta = 0;
  geo->GetOptD(nam, "theta", theta, GeoParser::Unit(rad));

  G4bool rotate_x = false;
  geo->GetOptB(nam, "rotate_x", rotate_x);

  if( rotate_x ) {
    fThetaX = theta;
  } else {
    fThetaY = theta;
  }

  cout << "TrkMapsBasicHits::LocalFromGeo, " << nam << ": ";
  cout << fXpos << " " << fYpos << " " << fZpos << " " << fThetaX << " " << fThetaY << endl;

}//LocalFromGeo

//_____________________________________________________________________________
void TrkMapsBasicHits::GlobalToLocal() {

  //transform hit positions from global to local coordinates

  //hits loop
  for(unsigned long i=0; i<fHitsR.size(); i++) {

    Hit& h = fHitsR[i];

    TVector3 pos(h.x-fXpos, h.y-fYpos, h.z-fZpos);
    pos.RotateY(-fThetaY);
    pos.RotateX(-fThetaX);

    h.x = pos.X();
    h.y = pos.Y();
    h.z = pos.Z();

  }//hits loop

}//GlobalToLocal














