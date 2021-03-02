
//_____________________________________________________________________________
//
// construction of individual detectors and components
// is here
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
#include "ComponentBuilder.h"

//detectors and components
#include "BoxCal.h"
#include "ExitWindow.h"
#include "Magnet.h"
#include "CompCal.h"
#include "Collimator.h"
#include "ExitWinZEUS.h"
#include "ExitWindowV1.h"
#include "ExitWindowV2.h"
#include "BeamMagnet.h"
#include "BeamMagnetV2.h"
#include "BoxCalV2.h"
#include "ConeAperture.h"
#include "CollimatorV2.h"
#include "CaloBPC.h"
#include "BeamQuadrupole.h"
#include "central_config.h"
#ifdef BUILD_CENTRAL
  #include "CentralBuilder.h"
#endif
#include "GraphiteFilter.h"
#include "TrackDet.h"
#include "CaloBuilder.h"

//_____________________________________________________________________________
ComponentBuilder::ComponentBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det):
  fTop(top), fGeo(geo), fDet(det) {

  for(unsigned int i=0; i<fGeo->GetN(); i++) AddDetector(i);

}//ComponentBuilder

//_____________________________________________________________________________
void ComponentBuilder::AddDetector(unsigned int i) {

  //add detector to all detectors

  //G4cout << "ComponentBuilder::AddDetector: " << fGeo->GetType(i) << " " << fGeo->GetName(i) << G4endl;

  //detector type and name
  G4String type = fGeo->GetType(i);
  G4String name = fGeo->GetName(i);

  //construct detector or component of type 'type'
  Detector *det = 0x0;

  if( type == "BoxCalV2" ) {
    det = new BoxCalV2(name, fGeo, fTop);

  } else if( type == "BeamMagnetV2" ) {
    det = new BeamMagnetV2(name, fGeo, fTop);

  } else if( type == "ExitWindowV2" ) {
    det = new ExitWindowV2(name, fGeo, fTop);

  } else if( type == "Collimator" ) {
    new Collimator(name, fGeo, fTop);

  } else if( type == "Magnet" ) {
    new Magnet(name, fGeo, fTop);

  } else if( type == "BoxCal" ) {
    det = new BoxCal(name, fGeo, fTop);

  } else if( type == "CompCal" ) {
    det = new CompCal(name, fGeo, fTop);

  } else if( type == "ConeAperture" ) {
    det = new ConeAperture(name, fGeo, fTop);

  } else if( type == "CollimatorV2" ) {
    det = new CollimatorV2(name, fGeo, fTop);

  } else if( type == "CaloBPC" ) {
    det = new CaloBPC(name, fGeo, fTop);

  } else if( type == "BeamQuadrupole" ) {
    det = new BeamQuadrupole(name, fGeo, fTop);

  } else if( type == "CentralDetector" ) {
    #ifdef BUILD_CENTRAL
      CentralBuilder central(fTop, fGeo, fDet);
    #endif

  } else if( type == "GraphiteFilter" ) {
    new GraphiteFilter(name, fGeo, fTop);

  } else if( type == "TrackDet" ) {
    det = new TrackDet(name, fGeo, fTop);

  } else if( type == "CaloBuilder" ) {
    CaloBuilder calo(fTop, fGeo, fDet);

  }

  if(!det) return;

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector

















