
//_____________________________________________________________________________
//
// main detector construction,
// detector definition is here
//_____________________________________________________________________________

//C++
#include <vector>
#include <algorithm>
#include <typeinfo>

//Geant
#include "G4GenericMessenger.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4Event.hh"
#include "G4VisAttributes.hh"
#include "G4SDManager.hh"

//local classes
#include "DetectorConstruction.h"
#include "RootOut.h"
#include "MCEvent.h"
#include "GeoParser.h"
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

//_____________________________________________________________________________
DetectorConstruction::DetectorConstruction() : G4VUserDetectorConstruction(), fDet(0), fOut(0),
    fGeo(0), fMsg(0) {

  G4cout << "DetectorConstruction::DetectorConstruction" << G4endl;

  //output file and tree
  fOut = new RootOut();

  //all detectors and their parts
  fDet = new std::vector<Detector*>;

  //MC event, also inherits from Detector
  fMC = new MCEvent();
  fMC->Add(fDet);

  //geometry parser
  fGeo = new GeoParser();

  //messenger for detectors and components
  fMsg = new G4GenericMessenger(this, "/lmon/construct/");
  fMsg->DeclareProperty("geometry", fGeoName);

}//DetectorConstruction

//_____________________________________________________________________________
DetectorConstruction::~DetectorConstruction() {

  //write the tree and close output file
  fOut->Close();

  delete fDet;

}//~DetectorConstruction

//_____________________________________________________________________________
G4VPhysicalVolume* DetectorConstruction::Construct() {

  G4cout << G4endl << "DetectorConstruction::Construct: " << fGeoName << G4endl;

  //run the geometry parser
  fGeo->LoadInput(fGeoName);

  //vacuum top material
  G4Material* top_m = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");

  //top world volume
  G4Box *top_s = new G4Box("top_s", 2*meter, 2*meter, 35*meter);
  //G4Box *top_s = new G4Box("top_s", 3*m, 3*m, 3*m);
  G4LogicalVolume *top_l = new G4LogicalVolume(top_s, top_m, "top_l");
  //top_l->SetVisAttributes( G4VisAttributes::GetInvisible() );
  G4VPhysicalVolume *top_p = new G4PVPlacement(0, G4ThreeVector(), top_l, "top_p", 0, false, 0);

  //add detectors and components
  for(unsigned int i=0; i<fGeo->GetN(); i++) AddDetector(i, top_l);

  return top_p;

}//Construct

//_____________________________________________________________________________
void DetectorConstruction::BeginEvent(const G4Event *evt) const {

  //detector loop for  ClearEvent  in each detector
  std::for_each(fDet->begin(), fDet->end(), std::mem_fun( &Detector::ClearEvent ));

  //set MC
  fMC->BeginEvent(evt);

}//BeginEvent

//_____________________________________________________________________________
void DetectorConstruction::FinishEvent() const {

  //detector loop
  std::for_each(fDet->begin(), fDet->end(), std::mem_fun( &Detector::FinishEvent ));

  //fill the output tree
  fOut->FillTree();

}//WriteEvent

//_____________________________________________________________________________
void DetectorConstruction::AddDetector(unsigned int i, G4LogicalVolume *top) {

  //add detector to all detectors

  //G4cout << "DetectorConstruction::AddDetector: " << fGeo->GetType(i) << " " << fGeo->GetName(i) << G4endl;

  //detector type and name
  G4String type = fGeo->GetType(i);
  G4String name = fGeo->GetName(i);

  //construct detector or component of type 'type'
  Detector *det = 0x0;

  if( type == "BoxCalV2" ) {
    det = new BoxCalV2(name, fGeo, top);

  } else if( type == "BeamMagnetV2" ) {
    det = new BeamMagnetV2(name, fGeo, top);

  } else if( type == "ExitWindowV2" ) {
    det = new ExitWindowV2(name, fGeo, top);

  } else if( type == "Collimator" ) {
    new Collimator(name, fGeo, top);

  } else if( type == "Magnet" ) {
    new Magnet(name, fGeo, top);

  } else if( type == "BoxCal" ) {
    det = new BoxCal(name, fGeo, top);

  } else if( type == "CompCal" ) {
    det = new CompCal(name, fGeo, top);

  }

  if(!det) return;

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector

//_____________________________________________________________________________
void DetectorConstruction::CreateOutput() const {

  //open output file
  fOut->Open();

  //detector loop to call CreateOutput
  std::vector<Detector*>::iterator i = fDet->begin();
  while(i != fDet->end()) {
    (*i++)->CreateOutput( fOut->GetTree() );
  }//detector loop

}//CreateOutput

//_____________________________________________________________________________
void DetectorConstruction::ConstructSDandField() {

  G4cout << "DetectorConstruction::ConstructSDandField" << G4endl;

  //detector loop
  std::vector<Detector*>::iterator i;
  for(i = fDet->begin(); i != fDet->end(); ++i) {
    Detector *det = *i;

    G4VSensitiveDetector *sd = dynamic_cast<G4VSensitiveDetector*>(det);
    if(!sd) continue;

    //detector inherits also from G4VSensitiveDetector, add it to Geant

    G4SDManager::GetSDMpointer()->AddNewDetector(sd);
    SetSensitiveDetector(det->GetName(), sd);

    G4cout << "  " << det->GetName() << G4endl;
  }//detector loop

}//ConstructSDandField



















