
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
#include "G4Step.hh"
#include "G4SystemOfUnits.hh"
#include "G4NavigationHistory.hh"

//local classes
#include "DetUtils.h"
#include "GeoParser.h"
#include "TrkMapsBasicHits.h"

using namespace std;

//_____________________________________________________________________________
TrkMapsBasicHits::TrkMapsBasicHits(): fXpos(0), fYpos(0), fZpos(0), fThetaX(0), fThetaY(0) {

}//ParticleCounterHits

//_____________________________________________________________________________
void TrkMapsBasicHits::AddSignal(G4Step *step) {

  //add signal for a given pixel

  //track ID and PDG in the step
  G4Track *track = step->GetTrack();
  G4int itrk = track->GetTrackID();
  G4int pdg = track->GetParticleDefinition()->GetPDGEncoding();

  //pixel location
  const G4TouchableHandle& hnd = step->GetPreStepPoint()->GetTouchableHandle();
  G4int ipix = hnd->GetCopyNumber(); // pixel index in the row
  G4int irow = hnd->GetCopyNumber(1); // row index in the layer

  //hit at a given pixel location
  map<pair<Int_t, Int_t>, Hit>::iterator it = fHitsW.find( pair(ipix, irow) );

  //new hit at a given location
  if( it == fHitsW.end() ) {

    //global pixel position
    G4ThreeVector origin(0, 0, 0);
    G4ThreeVector gpos = hnd->GetHistory()->GetTopTransform().Inverse().TransformPoint(origin);
    G4double x = gpos.x()/mm;
    G4double y = gpos.y()/mm;
    G4double z = gpos.z()/mm;

    //create the hit
    it = fHitsW.insert( make_pair(pair(ipix, irow), Hit(ipix, irow, x, y, z, itrk, pdg)) ).first;
  }

  //add deposited energy in the hit
  Hit& hit = (*it).second;
  hit.en += step->GetTotalEnergyDeposit()/keV;

  //lowest track ID associated with the hit and its PDG code
  if( itrk < hit.itrk ) {
    hit.itrk = itrk;
    hit.pdg = pdg;
  }

  //G4cout << itrk << " " << pdg <<  " " << ipix << " " << irow << " " << edep_in_step;
  //G4cout << " " << gpos.x()/mm << " " << gpos.y()/mm << " " << gpos.z()/mm << G4endl;

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

  DetUtils u(nam, tree);

  u.AddBranch("_HitIpix", fIpix);
  u.AddBranch("_HitIrow", fIrow);

  u.AddBranch("_HitX", fX);
  u.AddBranch("_HitY", fY);
  u.AddBranch("_HitZ", fZ);
  u.AddBranch("_HitEn", fEn);

  u.AddBranch("_HitItrk", fItrk);
  u.AddBranch("_HitPdg", fPdg);

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

    //G4cout << hit.itrk << " " << hit.pdg <<  " " << hit.ipix << " " << hit.irow << " " << hit.en;
    //G4cout << " " << hit.x << " " << hit.y << " " << hit.z << G4endl;

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

  tree->SetBranchAddress((nam+"_HitIpix").c_str(), &fIpix);
  tree->SetBranchAddress((nam+"_HitIrow").c_str(), &fIrow);

  tree->SetBranchAddress((nam+"_HitX").c_str(), &fX);
  tree->SetBranchAddress((nam+"_HitY").c_str(), &fY);
  tree->SetBranchAddress((nam+"_HitZ").c_str(), &fZ);
  tree->SetBranchAddress((nam+"_HitEn").c_str(), &fEn);

  tree->SetBranchAddress((nam+"_HitItrk").c_str(), &fItrk);
  tree->SetBranchAddress((nam+"_HitPdg").c_str(), &fPdg);

}//ConnectInput

//_____________________________________________________________________________
void TrkMapsBasicHits::LoadHits() {

  //load hits for a given event

  fHitsR.clear();

  //input vector loop
  for(unsigned long i=0; i<fIpix->size(); i++) {

    fHitsR.push_back( Hit(fIpix->at(i), fIrow->at(i), fX->at(i), fY->at(i), fZ->at(i), fItrk->at(i), fPdg->at(i)) );
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

  //cout << fXpos << " " << fYpos << " " << fZpos << " " << fThetaX << " " << fThetaY << endl;

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














