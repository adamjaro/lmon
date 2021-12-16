
//_____________________________________________________________________________
//
// construction of polarimetry detectors and components
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
#include "PolBuilder.h"

//local detectors and components
#include "PolTrackLay.h"
#include "PolCTarget.h"

//macros
#define ADD_DETECTOR(det) (fDets.insert( make_pair(#det, &PolBuilder::MakeDet<det>) ))
#define ADD_COMPONENT(comp) (fComp.insert( make_pair(#comp, &PolBuilder::MakeDet<comp>) ))

//_____________________________________________________________________________
PolBuilder::PolBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det):
  fTop(top), fGeo(geo), fDet(det) {

  //register the detectors
  ADD_DETECTOR(PolTrackLay);

  //register the components
  ADD_COMPONENT(PolCTarget);

  for(unsigned int i=0; i<fGeo->GetN(); i++) AddDetector(i);

}//PolBuilder

//_____________________________________________________________________________
void PolBuilder::AddDetector(unsigned int i) {

  //add detector or component

  //detector type and name
  G4String type = fGeo->GetType(i);
  G4String name = fGeo->GetName(i);

  //construct detector or component of type 'type'
  Detector *det = 0x0;

  //detector or component from factory
  std::map<G4String, MakeDetPtr>::iterator idet;

  //component
  idet = fComp.find(type);
  if( idet != fComp.end() ) {
    (this->*(*idet).second)(name, fGeo, fTop);
  }

  //detector
  idet = fDets.find(type);
  if( idet != fDets.end() ) {
    det = (this->*(*idet).second)(name, fGeo, fTop);
  }

  if(!det) return;

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector
















