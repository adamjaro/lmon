
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
#include "CalPWO.h"

//macros
#define ADD_DETECTOR(det) (fDets.insert( make_pair(#det, &CaloBuilder::MakeDet<det>) ))

//_____________________________________________________________________________
CaloBuilder::CaloBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det):
  fTop(top), fGeo(geo), fDet(det) {

  //individual detectors as defined here
  ADD_DETECTOR( HcalA262 );
  ADD_DETECTOR( UcalA290 );
  ADD_DETECTOR( WScFiZX );
  ADD_DETECTOR( WScFiZXv2 );
  ADD_DETECTOR( WScFiZXv3 );
  ADD_DETECTOR( CalPWO );

  for(unsigned int i=0; i<fGeo->GetN(); i++) AddDetector(i);

}//CaloBuilder

//_____________________________________________________________________________
void CaloBuilder::AddDetector(unsigned int i) {

  //add detector or component

  //detector type and name
  G4String type = fGeo->GetType(i);
  G4String name = fGeo->GetName(i);

  //factory detector construction
  std::map<G4String, MakeDetPtr>::iterator idet = fDets.find(type);
  if( idet == fDets.end() ) return;

  //add detector to all detectors
  Detector *det = (this->*(*idet).second)(name, fGeo, fTop);
  det->Add(fDet);

}//AddDetector
















