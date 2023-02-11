
//_____________________________________________________________________________
//
// Hits for optical detector, PMT or SiPM, version V2
// derived from the DetectorData template
//_____________________________________________________________________________

//C++
#include <iostream>

//ROOT
#include "TTree.h"

//Geant
#include "G4ios.hh"

//local classes
#include "PhotoHitsV2.h"

using namespace std;

//_____________________________________________________________________________
PhotoHitsV2::Coll::Coll() {

  G4cout << "PhotoHitsV2::Coll::Coll" << G4endl;

  //hits memory representation
  AddUnitAttr("_HitV2PosX", fUnitIO.pos_x);
  AddUnitAttr("_HitV2PosY", fUnitIO.pos_y);
  AddUnitAttr("_HitV2PosZ", fUnitIO.pos_z);
  AddUnitAttr("_HitV2Time", fUnitIO.time);

}//Coll

//_____________________________________________________________________________
PhotoHitsV2::Hit& PhotoHitsV2::Coll::CreateHit() {

  //make new hit and return reference to it

  fStorage.push_back( PhotoHitsV2::Hit() );

  return fStorage.back();

}//Coll::CreateHit



