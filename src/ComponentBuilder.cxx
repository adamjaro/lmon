
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
#include "BeamPipeV1.h"
#include "BoxSegment.h"
#include "ParticleCounter.h"
#include "VacB2lumiWin.h"
#include "VacDrift.h"
#include "VacTaggerWin.h"
#include "VacLumi.h"
#include "ConeBeam.h"
#include "BeamDrift.h"
#include "PolBuilder.h"
#include "CylBeam.h"
#include "CylSegment.h"
#include "TrkMapsBasic.h"

//macros
#define ADD_DETECTOR(det) (fDets.insert( make_pair(#det, &ComponentBuilder::MakeDet<det>) ))
#define ADD_COMPONENT(comp) (fComp.insert( make_pair(#comp, &ComponentBuilder::MakeDet<comp>) ))

//_____________________________________________________________________________
ComponentBuilder::ComponentBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det):
  fTop(top), fGeo(geo), fDet(det) {

  //beam components
  ADD_COMPONENT( BeamDrift );
  ADD_COMPONENT( ConeBeam );
  ADD_COMPONENT( CylBeam );
  ADD_COMPONENT( CylSegment );
  //fComp.insert( make_pair("Collimator", &ComponentBuilder::MakeDet< Collimator >) );
  //fComp.insert( make_pair("GraphiteFilter", &ComponentBuilder::MakeDet< GraphiteFilter >) );

  //vacuum segments
  ADD_COMPONENT( VacDrift );
  ADD_COMPONENT( VacTaggerWin );
  ADD_COMPONENT( VacB2lumiWin );
  ADD_COMPONENT( BoxSegment );
  ADD_COMPONENT( VacLumi );

  //detectors or active segments
  ADD_DETECTOR( ParticleCounter );
  ADD_DETECTOR( ExitWindowV1 );
  ADD_DETECTOR( ExitWindowV2 );
  ADD_DETECTOR( BeamMagnetV2 );
  ADD_DETECTOR( BeamQuadrupole );
  ADD_DETECTOR( Magnet );
  ADD_DETECTOR( BeamPipeV1 );
  ADD_DETECTOR( ConeAperture );
  ADD_DETECTOR( CollimatorV2 );
  ADD_DETECTOR( BoxCal );
  ADD_DETECTOR( BoxCalV2 );
  ADD_DETECTOR( CompCal );
  ADD_DETECTOR( CaloBPC );
  ADD_DETECTOR( TrackDet );
  ADD_DETECTOR( TrkMapsBasic );

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

  //non-factory parts
  if( type == "CaloBuilder" ) {
    CaloBuilder calo(fTop, fGeo, fDet);

  } else if( type == "CentralDetector" ) {
    #ifdef BUILD_CENTRAL
      CentralBuilder central(fTop, fGeo, fDet);
    #endif

  } else if( type == "Collimator" ) {
    new Collimator(name, fGeo, fTop);

  } else if( type == "GraphiteFilter" ) {
    new GraphiteFilter(name, fGeo, fTop);

  } else if( type == "PolBuilder" ) {
    PolBuilder pol(fTop, fGeo, fDet);

  }

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

















