
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
//#include "G4ios.hh"

//local classes
#include "PhotoHitsV2.h"

using namespace std;

//_____________________________________________________________________________
PhotoHitsV2::Coll::Coll() {

  //G4cout << "PhotoHitsV2::Coll::Coll" << G4endl;

  //hits memory representation, the names will be a suffix to the detector name
  AddUnitAttr("_HitPosX", fUnitIO.pos_x);
  AddUnitAttr("_HitPosY", fUnitIO.pos_y);
  AddUnitAttr("_HitPosZ", fUnitIO.pos_z);
  AddUnitAttr("_HitTime", fUnitIO.time);
  AddUnitAttr("_HitPmtX", fUnitIO.pmt_x);
  AddUnitAttr("_HitPmtY", fUnitIO.pmt_y);
  AddUnitAttr("_HitPmtZ", fUnitIO.pmt_z);
  AddUnitAttr("_HitCellID", fUnitIO.cell_id);
  AddUnitAttr("_HitPrimID", fUnitIO.prim_id);

}//Coll













