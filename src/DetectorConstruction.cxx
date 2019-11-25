
//_____________________________________________________________________________
//
// main detector construction,
// detector definition is here
//_____________________________________________________________________________

//C++
#include <vector>
#include <algorithm>
#include <typeinfo>

//ROOT
#include "TFile.h"
#include "TTree.h"
#include "TClass.h"
#include "TROOT.h"
#include "TSystem.h"

//Geant
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
#include "SensDetDummy.h"
#include "BoxCal.h"
#include "ExitWindow.h"
#include "Magnet.h"
#include "CompCal.h"
#include "Collimator.h"
#include "ExitWinZEUS.h"

//_____________________________________________________________________________
DetectorConstruction::DetectorConstruction() : G4VUserDetectorConstruction(), fDet(0), fPhotGen(0) {

  G4cout << "DetectorConstruction::DetectorConstruction" << G4endl;

  //inctruct ROOT not to write anything about G4VSensitiveDetector to file
  //by pointing it to an empty dummy class SensDetDummy
  if( gROOT->GetVersionInt() >= 60000 ) {
    // ROOT 6
    ROOT::AddClass("G4VSensitiveDetector", 0, typeid(SensDetDummy), TClass::GetDict("SensDetDummy"), 0);
  } else {
    // ROOT 5
    TClass::GetClass("SensDetDummy")->Clone("G4VSensitiveDetector");
  }

  //create the output file, name to come from Messenger
  gSystem->MakeDirectory("../data");
  fOut = new TFile("../data/lmon.root", "recreate");

  //output detector tree
  fDetTree = new TTree("DetectorTree", "DetectorTree");

  //all detectors and their parts
  fDet = new std::vector<Detector*>;

  //generated photon
  fPhotGen = new Double_t;

}//DetectorConstruction

//_____________________________________________________________________________
DetectorConstruction::~DetectorConstruction() {

  //write the tree
  fDetTree->Write();

  //close the output file
  fOut->Close();

  delete fDet;
  delete fPhotGen;

}//~DetectorConstruction

//_____________________________________________________________________________
G4VPhysicalVolume* DetectorConstruction::Construct() {

  G4cout << G4endl << "DetectorConstruction::Construct" << G4endl;

  //vacuum top material
  G4Material* top_m = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");

  //top world volume
  G4Box *top_s = new G4Box("top_s", 2*meter, 2*meter, 3500*cm);
  G4LogicalVolume *top_l = new G4LogicalVolume(top_s, top_m, "top_l");
  //top_l->SetVisAttributes( G4VisAttributes::GetInvisible() );
  G4VPhysicalVolume *top_p = new G4PVPlacement(0, G4ThreeVector(), top_l, "top_p", 0, false, 0);

  //photon exit window
  //new ExitWindow(-2000*cm, top_l); // only material
  AddDetector( new ExitWinZEUS("ExitWinZEUS", -2000*cm, top_l) ); // demonstrator to write detector as a branch

  //collimator
  new Collimator(-2137*cm, top_l);

  //dipole magnet
  new Magnet(-2250*cm, top_l);

  //detectors
  G4double dpos = -3135*cm;
  //AddDetector(new BoxCal("phot", dpos-50*cm, 0, top_l));
  //AddDetector(new BoxCal("up", dpos, 4.2*cm, top_l));
  //AddDetector(new BoxCal("down", dpos, -4.2*cm, top_l));

  AddDetector(new CompCal("phot", dpos-50*cm, 0, top_l));
  AddDetector(new CompCal("up", dpos, 4.2*cm, top_l));
  AddDetector(new CompCal("down", dpos, -4.2*cm, top_l));

  return top_p;

}//Construct

//_____________________________________________________________________________
void DetectorConstruction::FinishEvent(const G4Event *evt) const {

  //energy of generated gamma photon
  *fPhotGen = evt->GetPrimaryVertex()->GetPrimary()->GetTotalEnergy();

  //detector loop
  std::for_each(fDet->begin(), fDet->end(), std::mem_fun( &Detector::FinishEvent ));

  //fill the output tree
  fDetTree->Fill();

}//WriteEvent

//_____________________________________________________________________________
void DetectorConstruction::ClearEvent() const {

  //detector loop
  std::for_each(fDet->begin(), fDet->end(), std::mem_fun( &Detector::ClearEvent ));

}//ClearEvent

//_____________________________________________________________________________
void DetectorConstruction::AddDetector(Detector *det) {

  //add detector to all detectors
  det->Add(fDet);

}//AddDetector

//_____________________________________________________________________________
void DetectorConstruction::CreateOutput() const {

  //energy of generated gamma photon
  fDetTree->Branch("phot_gen", fPhotGen, "phot_gen/D");

  //output of the detectors

  //detector loop
  std::vector<Detector*>::iterator i = fDet->begin();
  while(i != fDet->end()) {
    (*i++)->CreateOutput(fDetTree);
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



















