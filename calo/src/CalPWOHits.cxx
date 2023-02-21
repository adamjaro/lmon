
//_____________________________________________________________________________
//
// Hits for CalPWO implementation of a PWO calorimeter
// derived from the DetectorData template
//_____________________________________________________________________________

//C++
#include <iostream>

//ROOT
#include "TTree.h"

//Geant
//#include "G4ios.hh"

//local classes
#include "CalPWOHits.h"

using namespace std;

//_____________________________________________________________________________
CalPWOHits::Coll::Coll() {

  //G4cout << "CalPWOHits::Coll::Coll" << G4endl;

  //hits memory representation, the names will be a suffix to the detector name
  AddUnitAttr("_HitCellID", fUnitIO.cell_id);
  AddUnitAttr("_HitCellX", fUnitIO.x);
  AddUnitAttr("_HitCellY", fUnitIO.y);
  AddUnitAttr("_HitCellZ", fUnitIO.z);
  AddUnitAttr("_HitEn", fUnitIO.en);
  AddUnitAttr("_HitPrimID", fUnitIO.prim_id);

}//Coll

//_____________________________________________________________________________
void CalPWOHits::Coll::FinishEvent() {

  //locate primary ID with the largest energy deposition and assing it for each hit

  using namespace CalPWOHits;

  //hit loop
  for(auto& ihit: fStorage) {

    Hit& h = ihit.second;

    Int_t id = -1;
    Double_t en = -1;

    //prim ID loop
    for(const auto& id_en: h.prim_energy) {

      if( id_en.second < en ) continue;

      //largest found energy deposition
      en = id_en.second;
      id = id_en.first;
    }

    //set primary ID to the hit
    h.prim_id = id;

    //clear the transient container
    h.prim_energy.clear();

  }//hit loop

  //finish for the hits
  DetectorData::FinishEvent();

}//FinishEvent































