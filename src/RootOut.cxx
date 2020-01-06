
//_____________________________________________________________________________
//
// helper class for ROOT TTree output
//_____________________________________________________________________________

//C++
#include <string>

//ROOT
#include "TFile.h"
#include "TTree.h"
#include "TClass.h"
#include "TROOT.h"
#include "TSystem.h"

//Geant
#include "G4GenericMessenger.hh"

//local classes
#include "RootOut.h"
#include "SensDetDummy.h"

using namespace std;

//_____________________________________________________________________________
RootOut::RootOut(): fOut(0), fDetTree(0) {

  //default name for output file
  fOutputName = "../data/lmon.root";

  //command for name of output file
  fMsg = new G4GenericMessenger(this, "/lmon/output/");
  fMsg->DeclareProperty("name", fOutputName);

  //inctruct ROOT not to write anything about G4VSensitiveDetector to file
  //by pointing it to an empty dummy class SensDetDummy
  if( gROOT->GetVersionInt() >= 60000 ) {
    // ROOT 6
    ROOT::AddClass("G4VSensitiveDetector", 0, typeid(SensDetDummy), TClass::GetDict("SensDetDummy"), 0);
  } else {
    // ROOT 5
    TClass::GetClass("SensDetDummy")->Clone("G4VSensitiveDetector");
  }

}//RootOut

//_____________________________________________________________________________
void RootOut::Open() {

  std::string nam(fOutputName.data());

  G4cout << "RootOut::Open, " << nam << G4endl;

  //create directory for the output
  if( nam.find_last_of("/") != string::npos ) {
    string dir = nam.substr(0, nam.find_last_of("/"));
    if(!dir.empty()) gSystem->MakeDirectory(dir.c_str());
  }

  //create the output file
  fOut = new TFile(nam.c_str(), "recreate");

  //test if file exists
  if(!fOut->IsOpen()) {
    G4String description = "Can't open output: " + fOutputName;
    G4Exception("DetectorConstruction::CreateOutput", "OutputNotOpen01", FatalException, description);
  }

  //output detector tree
  fDetTree = new TTree("DetectorTree", "DetectorTree");

}//Open

//_____________________________________________________________________________
void RootOut::FillTree() {

  fDetTree->Fill();

}//FillTree

//_____________________________________________________________________________
void RootOut::Close() {

  //write the tree
  if(fDetTree) fDetTree->Write();

  //close the output file
  if(fOut) fOut->Close();

}//Close

















