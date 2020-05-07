
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

//_____________________________________________________________________________
CentralBuilder::CentralBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det):
  fTop(top), fGeo(geo), fDet(det) {

  G4cout << "Hi from central builder" << G4endl;

}//CentralBuilder

