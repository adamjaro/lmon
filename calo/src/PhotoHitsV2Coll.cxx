
//C++
#include <iostream>

//ROOT
#include "TTree.h"

//Geant
#include "G4ios.hh"

//local classes
#include "PhotoHitsV2Coll.h"

using namespace std;

//_____________________________________________________________________________
PhotoHitsV2Coll::PhotoHitsV2Coll() {

  G4cout << "PhotoHitsV2Coll::PhotoHitsV2Coll" << G4endl;

  //hits memory representation
  AddUnitAttr("_HitV2PosX", fUnitIO.pos_x);
  AddUnitAttr("_HitV2PosY", fUnitIO.pos_y);
  AddUnitAttr("_HitV2PosZ", fUnitIO.pos_z);
  AddUnitAttr("_HitV2Time", fUnitIO.time);

}//PhotoHitsV2Coll

