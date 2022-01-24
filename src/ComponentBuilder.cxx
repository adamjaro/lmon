
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
  fComp.insert( make_pair("VacDrift", &ComponentBuilder::MakeDet< VacDrift >) );
  fComp.insert( make_pair("VacTaggerWin", &ComponentBuilder::MakeDet< VacTaggerWin >) );
  fComp.insert( make_pair("VacB2lumiWin", &ComponentBuilder::MakeDet< VacB2lumiWin >) );
  fComp.insert( make_pair("BoxSegment", &ComponentBuilder::MakeDet< BoxSegment >) );
  fComp.insert( make_pair("VacLumi", &ComponentBuilder::MakeDet< VacLumi >) );
  //fComp.insert( make_pair("", &ComponentBuilder::MakeDet<  >) );

  //detectors or active segments
  fDets.insert( make_pair("ParticleCounter", &ComponentBuilder::MakeDet< ParticleCounter >) );
  fDets.insert( make_pair("ExitWindowV1", &ComponentBuilder::MakeDet< ExitWindowV1 >) );
  fDets.insert( make_pair("ExitWindowV2", &ComponentBuilder::MakeDet< ExitWindowV2 >) );
  fDets.insert( make_pair("BeamMagnetV2", &ComponentBuilder::MakeDet< BeamMagnetV2 >) );
  fDets.insert( make_pair("BeamQuadrupole", &ComponentBuilder::MakeDet< BeamQuadrupole >) );
  fDets.insert( make_pair("Magnet", &ComponentBuilder::MakeDet< Magnet >) );
  fDets.insert( make_pair("BeamPipeV1", &ComponentBuilder::MakeDet< BeamPipeV1 >) );
  fDets.insert( make_pair("ConeAperture", &ComponentBuilder::MakeDet< ConeAperture >) );
  fDets.insert( make_pair("CollimatorV2", &ComponentBuilder::MakeDet< CollimatorV2 >) );
  fDets.insert( make_pair("BoxCal", &ComponentBuilder::MakeDet< BoxCal >) );
  fDets.insert( make_pair("BoxCalV2", &ComponentBuilder::MakeDet< BoxCalV2 >) );
  fDets.insert( make_pair("CompCal", &ComponentBuilder::MakeDet< CompCal >) );
  fDets.insert( make_pair("CaloBPC", &ComponentBuilder::MakeDet< CaloBPC >) );
  fDets.insert( make_pair("TrackDet", &ComponentBuilder::MakeDet< TrackDet >) );
  //fDets.insert( make_pair("", &ComponentBuilder::MakeDet<  >) );

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

















