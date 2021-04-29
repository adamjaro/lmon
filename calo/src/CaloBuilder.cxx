
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
#include "CaloBuilder.h"

//local detectors and components
#include "HcalA262.h"
#include "UcalA290.h"
#include "WScFiZX.h"
#include "WScFiZXv2.h"
#include "WScFiZXv3.h"

//_____________________________________________________________________________
CaloBuilder::CaloBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det):
  fTop(top), fGeo(geo), fDet(det) {

  for(unsigned int i=0; i<fGeo->GetN(); i++) AddDetector(i);

}//CaloBuilder

//_____________________________________________________________________________
void CaloBuilder::AddDetector(unsigned int i) {

  //add detector or component

  //detector type and name
  G4String type = fGeo->GetType(i);
  G4String name = fGeo->GetName(i);

  //construct detector or component of type 'type'
  Detector *det = 0x0;

  if( type == "HcalA262" ) {
    det = new HcalA262(name, fGeo, fTop);

  } else if( type == "UcalA290" ) {
    det = new UcalA290(name, fGeo, fTop);

  } else if( type == "WScFiZX" ) {
    det = new WScFiZX(name, fGeo, fTop);

  } else if( type == "WScFiZXv2" ) {
    det = new WScFiZXv2(name, fGeo, fTop);

  } else if( type == "WScFiZXv3" ) {
    det = new WScFiZXv3(name, fGeo, fTop);

  }

  if(!det) return;

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector
















