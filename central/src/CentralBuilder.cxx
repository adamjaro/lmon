
//_____________________________________________________________________________
//
// construction of central detectors and components
//
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT
#include "Rtypes.h"

//Geant
#include "G4LogicalVolume.hh"

//local classes
#include "Detector.h"
#include "GeoParser.h"
#include "CentralBuilder.h"

//detectors and components
#include "BoxCalR.h"
#include "SolenoidBeAST.h"

//_____________________________________________________________________________
CentralBuilder::CentralBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det):
  fTop(top), fGeo(geo), fDet(det) {

  for(unsigned int i=0; i<fGeo->GetN(); i++) AddDetector(i);

}//CentralBuilder

//_____________________________________________________________________________
void CentralBuilder::AddDetector(unsigned int i) {

  //add detector or component

  //detector type and name
  G4String type = fGeo->GetType(i);
  G4String name = fGeo->GetName(i);

  //construct detector or component of type 'type'
  Detector *det = 0x0;

  //static G4LogicalVolume *solenoid_vol = 0; // solenoid volume

  if( type == "SolenoidBeAST" ) {
    new SolenoidBeAST(name, fGeo, fTop);
    //SolenoidBeAST *sol = new SolenoidBeAST(name, fGeo, fTop);
    //solenoid_vol = sol->GetLogicalVolume();

  } else if( type == "BoxCalR" ) {
    det = new BoxCalR(name, fGeo, fTop);
    //det = new BoxCalR(name, fGeo, solenoid_vol);

  }

  if(!det) return;

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector
















