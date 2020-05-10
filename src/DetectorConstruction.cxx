
//_____________________________________________________________________________
//
// main detector construction
//
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
#include "ComponentBuilder.h"

//_____________________________________________________________________________
DetectorConstruction::DetectorConstruction() : G4VUserDetectorConstruction(), fDet(0), fOut(0), fMsg(0) {

  G4cout << "DetectorConstruction::DetectorConstruction" << G4endl;

  //output file and tree
  fOut = new RootOut();

  //all detectors and their parts
  fDet = new std::vector<Detector*>;

  //MC event, also inherits from Detector
  fMC = new MCEvent();
  fMC->Add(fDet);

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
  GeoParser geo;
  geo.LoadInput(fGeoName);

  //create the top volume
  G4String topnam = geo.GetTopName();
  G4double topx = geo.GetD(topnam, "xsiz") * mm;
  G4double topy = geo.GetD(topnam, "ysiz") * mm;
  G4double topz = geo.GetD(topnam, "zsiz") * mm;

  //top world volume
  G4Box *top_s = new G4Box(topnam+"_s", topx, topy, topz);

  //vacuum top material
  G4Material* top_m = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *top_l = new G4LogicalVolume(top_s, top_m, topnam+"_l");
  //top_l->SetVisAttributes( G4VisAttributes::GetInvisible() );

  G4VPhysicalVolume *top_p = new G4PVPlacement(0, G4ThreeVector(), top_l, topnam+"_p", 0, false, 0);

  //add detectors and components
  ComponentBuilder builder(top_l, &geo, fDet);

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

  //G4cout << "DetectorConstruction::FinishEvent" << G4endl;
  //G4cout << G4endl;

}//FinishEvent

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



















