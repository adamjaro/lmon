
//_____________________________________________________________________________
//
// Hits for CaloBPC
//
//_____________________________________________________________________________

//C++
#include <map>
#include <vector>

//ROOT
#include "TTree.h"

//Geant
#include "G4SystemOfUnits.hh"
#include "G4String.hh"
#include "G4ios.hh"
#include "globals.hh"

//local classes
#include "DetUtils.h"
#include "CaloBPCHits.h"

using namespace std;

//_____________________________________________________________________________
void CaloBPCHits::SetScinPos(G4int istrip, G4double pos) {

  //scintillator position for a given strip index

  fXYpos.insert(make_pair(istrip, pos));

}//CaloBPCHits

//_____________________________________________________________________________
void CaloBPCHits::AddSignal(G4int istrip, G4int ilay, G4double en) {

  //add signal for vertical or horizontal scintillator

  //vertical or horizontal
  bool ver = ilay%2 == 0 ? true : false;

  //select the run-time hits and set the position
  map<Int_t, Hit> *hits = 0x0;
  Double_t xpos = 0., ypos = 0.;
  if( ver ) {
    hits = &fVerHits;
    xpos = fXYpos[istrip];
  } else {
    hits = &fHorHits;
    ypos = fXYpos[istrip];
  }

  //create hit for a given set of vertical or horizontal scintillators if not present
  map<Int_t, Hit>::iterator it = hits->find(istrip);
  if( it == hits->end() ) {
    it = hits->insert( make_pair(istrip, Hit(istrip, ver, xpos, ypos)) ).first;
  }

  //add deposited energy for a given hit
  Hit& hit = (*it).second;
  hit.en += en;

}//AddSignal

//_____________________________________________________________________________
void CaloBPCHits::ClearEvent() {

  //clear run-time hits and output representations

  fVerHits.clear();
  fHorHits.clear();

  fIscin->clear();
  fVert->clear();
  fEn->clear();
  fX->clear();
  fY->clear();
  fZ->clear();

}//ClearEvent

//_____________________________________________________________________________
void CaloBPCHits::FinishEvent() {

  //write for vertical and horizontal hits

  WriteHits(&fVerHits);
  WriteHits(&fHorHits);

}//FinishEvent

//_____________________________________________________________________________
void CaloBPCHits::WriteHits(map<Int_t, Hit> *hits) {

  //put hits to output vectors

  for(map<Int_t, Hit>::iterator i = hits->begin(); i != hits->end(); i++) {

    const Hit& hit = (*i).second;

    //G4cout << hit.iscin << " " << hit.vert << " " << hit.en << " " << hit.x << " " << hit.y << G4endl;

    fIscin->push_back( hit.iscin );
    fVert->push_back( hit.vert );
    fEn->push_back( hit.en );
    fX->push_back( hit.x );
    fY->push_back( hit.y );
    fZ->push_back( hit.z );

  }

}//WriteHits

//_____________________________________________________________________________
void CaloBPCHits::CreateOutput(G4String nam, TTree *tree) {

  //output from CaloBPCHits

  fIscin = new vector<Int_t>();
  fVert = new vector<Bool_t>();
  fEn = new vector<Double_t>();
  fX = new vector<Double_t>();
  fY = new vector<Double_t>();
  fZ = new vector<Double_t>();

  DetUtils u(nam, tree);

  u.AddBranch("_HitIscin", fIscin);
  u.AddBranch("_HitVert", fVert);
  u.AddBranch("_HitEn", fEn);
  u.AddBranch("_HitX", fX);
  u.AddBranch("_HitY", fY);
  u.AddBranch("_HitZ", fZ);

}//CreateOutput

//_____________________________________________________________________________
void CaloBPCHits::ConnectInput(string nam, TTree *tree) {

  //connect hits from input tree

  fIscin = 0x0;
  fVert = 0x0;
  fEn = 0x0;
  fX = 0x0;
  fY = 0x0;
  fZ = 0x0;

  tree->SetBranchAddress((nam+"_HitIscin").c_str(), &fIscin);
  tree->SetBranchAddress((nam+"_HitVert").c_str(), &fVert);
  tree->SetBranchAddress((nam+"_HitEn").c_str(), &fEn);
  tree->SetBranchAddress((nam+"_HitX").c_str(), &fX);
  tree->SetBranchAddress((nam+"_HitY").c_str(), &fY);
  tree->SetBranchAddress((nam+"_HitZ").c_str(), &fZ);

}//ConnectInput

//_____________________________________________________________________________
void CaloBPCHits::LoadHits() {

  //load hits for a given event

  fHits.clear();

  //vector loop
  for(unsigned long i=0; i<fIscin->size(); i++) {

    //set the hit from vectors
    fHits.push_back( Hit(fIscin->at(i), fVert->at(i), fX->at(i), fY->at(i)) );
    fHits.back().en = fEn->at(i);

  }//vector loop

}//LoadHits


































