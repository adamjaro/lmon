
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
#include "globals.hh"

//local classes
#include "RootOut.h"
#include "SensDetDummy.h"

using namespace std;

//_____________________________________________________________________________
RootOut::RootOut(): fOut(0), fDetTree(0) {

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
bool RootOut::Open(std::string nam) {

  G4cout << "RootOut::Open, " << nam << G4endl;

  //create directory for the output
  if( nam.find_last_of("/") != string::npos ) {
    string dir = nam.substr(0, nam.find_last_of("/"));
    if(!dir.empty()) gSystem->MakeDirectory(dir.c_str());
  }

  //create the output file
  fOut = new TFile(nam.c_str(), "recreate");

  //output detector tree
  fDetTree = new TTree("DetectorTree", "DetectorTree");

  return fOut->IsOpen();

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

















