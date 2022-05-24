
//_____________________________________________________________________________
//
// Hits for ParticleCounter
//
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT
#include "TTree.h"
#include "TVector3.h"

//Geant
#include "G4SystemOfUnits.hh"
#include "G4String.hh"
#include "G4ios.hh"
#include "globals.hh"

//local classes
#include "GeoParser.h"
#include "DetUtils.h"
#include "ParticleCounterHits.h"

using namespace std;

//_____________________________________________________________________________
ParticleCounterHits::ParticleCounterHits(): fXpos(0), fYpos(0), fZpos(0), fTheta_x(0), fTheta_y(0) {

}//ParticleCounterHits

//_____________________________________________________________________________
void ParticleCounterHits::AddHit() {

  //G4cout << "AddHit: " << fHit.pdg << G4endl;

  fHitPdg->push_back( fHit.pdg );
  fHitEn->push_back( fHit.en );
  fHitX->push_back( fHit.x );
  fHitY->push_back( fHit.y );
  fHitZ->push_back( fHit.z );
  fHitParentID->push_back( fHit.parentID );
  fHitItrk->push_back( fHit.itrk );
  fHitPrim->push_back( fHit.is_prim );

}//AddHit

//_____________________________________________________________________________
void ParticleCounterHits::CreateOutput(G4String nam, TTree *tree) {

  //output from ParticleCounterHits

  fHitPdg = new vector<Int_t>();
  fHitEn = new vector<Float_t>();
  fHitX = new vector<Float_t>();
  fHitY = new vector<Float_t>();
  fHitZ = new vector<Float_t>();
  fHitParentID = new vector<Int_t>();
  fHitItrk = new vector<Int_t>();
  fHitPrim = new vector<Bool_t>();

  DetUtils u(nam, tree);

  u.AddBranch("_HitPdg", fHitPdg);
  u.AddBranch("_HitEn", fHitEn);
  u.AddBranch("_HitX", fHitX);
  u.AddBranch("_HitY", fHitY);
  u.AddBranch("_HitZ", fHitZ);
  u.AddBranch("_HitParentID", fHitParentID);
  u.AddBranch("_HitItrk", fHitItrk);
  u.AddBranch("_HitPrim", fHitPrim);

}//CreateOutput

//_____________________________________________________________________________
void ParticleCounterHits::ClearEvent() {

  fHitPdg->clear();
  fHitEn->clear();
  fHitX->clear();
  fHitY->clear();
  fHitZ->clear();
  fHitParentID->clear();
  fHitItrk->clear();
  fHitPrim->clear();

}//ClearEvent

//_____________________________________________________________________________
void ParticleCounterHits::ConnectInput(string nam, TTree *tree) {

  fHitPdg = 0x0;
  fHitEn = 0x0;
  fHitX = 0x0;
  fHitY = 0x0;
  fHitZ = 0x0;
  fHitParentID = 0x0;
  fHitItrk = 0x0;
  fHitPrim = 0x0;

  tree->SetBranchAddress((nam+"_HitPdg").c_str(), &fHitPdg);
  tree->SetBranchAddress((nam+"_HitEn").c_str(), &fHitEn);
  tree->SetBranchAddress((nam+"_HitX").c_str(), &fHitX);
  tree->SetBranchAddress((nam+"_HitY").c_str(), &fHitY);
  tree->SetBranchAddress((nam+"_HitZ").c_str(), &fHitZ);
  tree->SetBranchAddress((nam+"_HitParentID").c_str(), &fHitParentID);
  tree->SetBranchAddress((nam+"_HitItrk").c_str(), &fHitItrk);
  tree->SetBranchAddress((nam+"_HitPrim").c_str(), &fHitPrim);

}//ConnectInput

//_____________________________________________________________________________
ParticleCounterHits::CounterHit ParticleCounterHits::GetHit(int i) {

  ParticleCounterHits::CounterHit hit;

  hit.pdg = fHitPdg->at(i);
  hit.en = fHitEn->at(i);
  hit.x = fHitX->at(i);
  hit.y = fHitY->at(i);
  hit.z = fHitZ->at(i);
  hit.parentID = fHitParentID->at(i);
  hit.itrk = fHitItrk->at(i);
  hit.is_prim = fHitPrim->at(i);

  return hit;

}//GetHit

//_____________________________________________________________________________
void ParticleCounterHits::LocalFromGeo(G4String nam, GeoParser *geo) {

  //counter position from geometry

  geo->GetOptD(nam, "xpos", fXpos, GeoParser::Unit(mm));
  geo->GetOptD(nam, "ypos", fYpos, GeoParser::Unit(mm));
  geo->GetOptD(nam, "zpos", fZpos, GeoParser::Unit(mm));

  G4double theta = 0;
  geo->GetOptD(nam, "theta", theta, GeoParser::Unit(rad));

  G4bool rotate_x = false;
  geo->GetOptB(nam, "rotate_x", rotate_x);

  if( rotate_x ) {
    fTheta_x = theta;
  } else {
    fTheta_y = theta;
  }

}//LocalFromGeo

//_____________________________________________________________________________
ParticleCounterHits::CounterHit ParticleCounterHits::GlobalToLocal(CounterHit in) {

  CounterHit hit(in);

  TVector3 pos(in.x-fXpos, in.y-fYpos, in.z-fZpos);
  pos.RotateY(-fTheta_y);
  pos.RotateX(-fTheta_x);

  hit.x = pos.X();
  hit.y = pos.Y();
  hit.z = pos.Z();

  return hit;

}//GlobalToLocal


























