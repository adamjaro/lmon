
//_____________________________________________________________________________
//
// Tagger station composed of as set of counting planes
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>

//ROOT
#include "TTree.h"
#include "TMath.h"

//Geant
#include "G4String.hh"

//local classes
#include "TagCounterPlane.h"
#include "TagCounter.h"

using namespace std;

//_____________________________________________________________________________
TagCounter::TagCounter(string nam, TTree *tree , TTree *otree, GeoParser *geo):
    fNam(nam), fIsHit(0), fNPlane(0), fSTree(0x0) {

    //planes for the station, A, B and C
    fPlanes.push_back( new TagCounterPlane(fNam+"A", tree, geo) );
    fPlanes.push_back( new TagCounterPlane(fNam+"B", tree, geo) );
    fPlanes.push_back( new TagCounterPlane(fNam+"C", tree, geo) );

    //branches for output tree
    otree->Branch((fNam+"_IsHit").c_str(), &fIsHit, (fNam+"_IsHit/O").c_str());
    otree->Branch((fNam+"_NPlane").c_str(), &fNPlane, (fNam+"_NPlane/I").c_str());

}//TagCounter

//_____________________________________________________________________________
void TagCounter::ProcessEvent() {

  fNPlane = 0;
  fIsHit = kTRUE;

  //planes loop
  for(unsigned int i=0; i<fPlanes.size(); i++) {

    fIsHit = fIsHit && fPlanes[i]->IsHit();

    if( !fPlanes[i]->IsHit() ) continue;
    fNPlane++;

  }//planes loop

  if( !fIsHit ) return;

  //hits in planes in event
  fNA = fPlanes[0]->GetNhit();
  fNB = fPlanes[1]->GetNhit();
  fNC = fPlanes[2]->GetNhit();

  //planes for track parameters
  TagCounterPlane *p0 = fPlanes[2];
  TagCounterPlane *p1 = fPlanes[0];

  //track angle in x and y
  fX = p1->GetX();
  fY = p1->GetY();
  fZ = p1->GetZ();
  fThetaX = GetTheta(p0->GetX(), p0->GetZ(), p1->GetX(), p1->GetZ());
  fThetaY = GetTheta(p0->GetY(), p0->GetZ(), p1->GetY(), p1->GetZ());

  if(fSTree) fSTree->Fill();

}//ProcessEvent

//_____________________________________________________________________________
Double_t TagCounter::GetTheta(Double_t xy0, Double_t z0, Double_t xy1, Double_t z1) {

  //track angle from two its points

  return TMath::ATan( (xy1-xy0)/(z1-z0) );

}//GetTheta

//_____________________________________________________________________________
void TagCounter::CreateOutput(bool create_planes) {

  //create output tree for a given station
  fSTree = new TTree(fNam.c_str(), fNam.c_str());
  fSTree->Branch("x", &fX, "x/D");
  fSTree->Branch("y", &fY, "y/D");
  fSTree->Branch("z", &fZ, "z/D");
  fSTree->Branch("theta_x", &fThetaX, "theta_x/D");
  fSTree->Branch("theta_y", &fThetaY, "theta_y/D");
  fSTree->Branch("nA", &fNA, "nA/I");
  fSTree->Branch("nB", &fNB, "nB/I");
  fSTree->Branch("nC", &fNC, "nC/I");

  //output for planes
  if(create_planes) {
    for_each(fPlanes.begin(), fPlanes.end(), mem_fn( &TagCounterPlane::CreateOutput ));
  }

}//CreateOutput

//_____________________________________________________________________________
void TagCounter::AddOutputBranch(string nam, Double_t *val) {

  //add a branch to the station output tree

  fSTree->Branch(nam.c_str(), val, (nam+"/D").c_str());

}//AddOutputBranch

//_____________________________________________________________________________
void TagCounter::WriteOutputs() {

  //output for the station
  if(fSTree) fSTree->Write();

  //output for individual planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fn( &TagCounterPlane::WriteOutputs ));

}//write_outputs






















