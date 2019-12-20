
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
#include "BoxCal.h"
#include "ExitWindow.h"
#include "Magnet.h"
#include "CompCal.h"
#include "Collimator.h"
#include "ExitWinZEUS.h"
#include "ExitWindowV1.h"

//_____________________________________________________________________________
DetectorConstruction::DetectorConstruction() : G4VUserDetectorConstruction(), fDet(0), fOut(0) {

  G4cout << "DetectorConstruction::DetectorConstruction" << G4endl;

  //default name for output file
  fOutputName = "../data/lmon.root";

  //command for name of output file
  fMsg = new G4GenericMessenger(this, "/lmon/output/");
  fMsg->DeclareProperty("name", fOutputName);

  //output file and tree
  fOut = new RootOut();

  //all detectors and their parts
  fDet = new std::vector<Detector*>;

  //MC event, also inherits from Detector
  fMC = new MCEvent();
  AddDetector(fMC);

}//DetectorConstruction

//_____________________________________________________________________________
DetectorConstruction::~DetectorConstruction() {

  //write the tree and close output file
  fOut->Close();

  delete fDet;

}//~DetectorConstruction

//_____________________________________________________________________________
G4VPhysicalVolume* DetectorConstruction::Construct() {

  G4cout << G4endl << "DetectorConstruction::Construct" << G4endl;

  //vacuum top material
  G4Material* top_m = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");

  //top world volume
  G4Box *top_s = new G4Box("top_s", 2*meter, 2*meter, 3500*cm);
  //G4Box *top_s = new G4Box("top_s", 3*m, 3*m, 3*m);
  G4LogicalVolume *top_l = new G4LogicalVolume(top_s, top_m, "top_l");
  //top_l->SetVisAttributes( G4VisAttributes::GetInvisible() );
  G4VPhysicalVolume *top_p = new G4PVPlacement(0, G4ThreeVector(), top_l, "top_p", 0, false, 0);

  //photon exit window
  //new ExitWindow(-2000*cm, top_l); // only material
  //AddDetector( new ExitWinZEUS("ExitWinZEUS", -2000*cm, top_l) ); // demonstrator to write detector as a branch
  AddDetector( new ExitWindowV1("ew", -21.7*meter, ExitWindowV1::kFlat, top_l) ); // v1 with output on pair conversion
  //AddDetector( new ExitWindowV1("ew", -20250.*mm, ExitWindowV1::kTilt, top_l) );

  //collimator
  //new Collimator(-2137*cm, top_l);

  //dipole magnet
  //new Magnet(-2250*cm, top_l);

  //detectors
  //G4double dpos = -3135*cm;
  //AddDetector(new BoxCal("phot", dpos-50*cm, 0, top_l));
  //AddDetector(new BoxCal("up", dpos, 4.2*cm, top_l));
  //AddDetector(new BoxCal("down", dpos, -4.2*cm, top_l));

  //AddDetector(new CompCal("phot", dpos-50*cm, 0, top_l));
  //AddDetector(new CompCal("up", dpos, 4.2*cm, top_l));
  //AddDetector(new CompCal("down", dpos, -4.2*cm, top_l));

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
void DetectorConstruction::AddDetector(Detector *det) {

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector

//_____________________________________________________________________________
void DetectorConstruction::CreateOutput() const {

  //open output file
  bool is_open = fOut->Open(fOutputName);

  //test if file exists
  if(!is_open) {
    G4String description = "Can't open output: " + fOutputName;
    G4Exception("DetectorConstruction::CreateOutput", "OutputNotOpen01", FatalException, description);
  }

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



















