
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

  DetUtils u(nam, tree);

  u.AddBranch("_HitPdg", fHitPdg);
  u.AddBranch("_HitEn", fHitEn);
  u.AddBranch("_HitX", fHitX);
  u.AddBranch("_HitY", fHitY);
  u.AddBranch("_HitZ", fHitZ);
  u.AddBranch("_HitParentID", fHitParentID);

}//CreateOutput

//_____________________________________________________________________________
void ParticleCounterHits::ClearEvent() {

  fHitPdg->clear();
  fHitEn->clear();
  fHitX->clear();
  fHitY->clear();
  fHitZ->clear();
  fHitParentID->clear();

}//ClearEvent

//_____________________________________________________________________________
void ParticleCounterHits::ConnectInput(string nam, TTree *tree) {

  fHitPdg = 0x0;
  fHitEn = 0x0;
  fHitX = 0x0;
  fHitY = 0x0;
  fHitZ = 0x0;
  fHitParentID = 0x0;

  tree->SetBranchAddress((nam+"_HitPdg").c_str(), &fHitPdg);
  tree->SetBranchAddress((nam+"_HitEn").c_str(), &fHitEn);
  tree->SetBranchAddress((nam+"_HitX").c_str(), &fHitX);
  tree->SetBranchAddress((nam+"_HitY").c_str(), &fHitY);
  tree->SetBranchAddress((nam+"_HitZ").c_str(), &fHitZ);
  tree->SetBranchAddress((nam+"_HitParentID").c_str(), &fHitParentID);

}//ConnectInput

//_____________________________________________________________________________
ParticleCounterHits::CounterHit& ParticleCounterHits::LoadHit(int i) {

  fHit.pdg = fHitPdg->at(i);
  fHit.en = fHitEn->at(i);
  fHit.x = fHitX->at(i);
  fHit.y = fHitY->at(i);
  fHit.z = fHitZ->at(i);
  fHit.parentID = fHitParentID->at(i);

  return fHit;

}//LoadHit

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
void ParticleCounterHits::GlobalToLocal() {

  TVector3 pos(fHit.x-fXpos, fHit.y-fYpos, fHit.z-fZpos);
  pos.RotateY(-fTheta_y);
  pos.RotateX(-fTheta_x);

  fHit.x = pos.X();
  fHit.y = pos.Y();
  fHit.z = pos.Z();

}//GlobalToLocal

























