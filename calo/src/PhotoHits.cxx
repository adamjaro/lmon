
//_____________________________________________________________________________
//
// Hits for optical detector, PMT or SiPM
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <algorithm>

//ROOT
#include "TTree.h"

//Geant
#include "G4ios.hh"
#include "G4String.hh"

//local classes
#include "PhotoHits.h"

using namespace std;

//_____________________________________________________________________________
PhotoHits::PhotoHits() {

  //hits memory representation
  fHitPars.push_back( new HitPar<Double_t>("_HitPosX", fHitIO.pos_x) );
  fHitPars.push_back( new HitPar<Double_t>("_HitPosY", fHitIO.pos_y) );
  fHitPars.push_back( new HitPar<Double_t>("_HitPosZ", fHitIO.pos_z) );
  fHitPars.push_back( new HitPar<Double_t>("_HitTime", fHitIO.time) );

}//PhotoHits

//_____________________________________________________________________________
void PhotoHits::CreateOutput(G4String nam, TTree *tree) {

  //hit representation loop
  for(HitParBase *i: fHitPars) {
    i->CreateOutput(nam, tree);
  }//hit representation loop

}//CreateOutput

//_____________________________________________________________________________
void PhotoHits::ClearEvent() {

  //clear run-time hits and the memory representation
  fHits.clear();
  for_each(fHitPars.begin(), fHitPars.end(), mem_fn( &HitParBase::ClearEvent ));

}//ClearEvent

//_____________________________________________________________________________
void PhotoHits::FinishEvent() {

  //hit loop
  for(Hit i: fHits) {

    //set the IO member
    fHitIO = i;

    //write the hit in all its representation parameters
    for_each(fHitPars.begin(), fHitPars.end(), mem_fn( &HitParBase::Write ));
  }//hit loop

}//FinishEvent

//_____________________________________________________________________________
void PhotoHits::ConnectInput(std::string nam, TTree *tree) {

  //hit representation loop
  for(HitParBase *i: fHitPars) {
    i->ConnectInput(nam, tree);
  }//hit representation loop

}//ConnectInput

//_____________________________________________________________________________
void PhotoHits::LoadHits() {

  //clear the run-time hits for the event
  fHits.clear();

  //hit loop
  for(unsigned long ihit = 0; ihit < fHitPars.front()->GetN(); ihit++) {

    //parameter representation loop
    for(HitParBase *ipar: fHitPars) {
      ipar->LoadVal(ihit);
    }//parameter representation loop

    //make the hit from the loaded parameters
    fHits.push_back( Hit(fHitIO) );
  }//hit loop

}//LoadHits


















