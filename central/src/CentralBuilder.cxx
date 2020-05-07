
//_____________________________________________________________________________
//
// construction of central detectors and components
//
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT

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

  if( type == "BoxCalR" ) {
    det = new BoxCalR(name, fGeo, fTop);

  } else if( type == "SolenoidBeAST" ) {
    new SolenoidBeAST(name, fGeo, fTop);

  }

  if(!det) return;

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector
















