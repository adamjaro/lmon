
//_____________________________________________________________________________
//
// simple reader for ExitWinZEUS,
// prints position of gamma when entering the exit window
//
// to be run as   root -l -b -q run_reader.C
//_____________________________________________________________________________

//C++
#include <iostream>
#include <typeinfo>

//ROOT
#include "TFile.h"
#include "TTree.h"
#include "TClass.h"
#include "TROOT.h"

//local headers
#include "SensDetDummy.h"
#include "ExitWinZEUS.h"

using namespace std;

//_____________________________________________________________________________
void reader() {

  //override for G4VSensitiveDetector
  if( gROOT->GetVersionInt() >= 60000 ) {
    // ROOT 6
    ROOT::AddClass("G4VSensitiveDetector", 0, typeid(SensDetDummy), TClass::GetDict("SensDetDummy"), 0);
  } else {
    // ROOT 5
    gROOT->GetClass("G4VSensitiveDetector");
  }

  //input
  TFile *infile = TFile::Open("../../data/lmon.root");

  //get tree from file
  TTree *dtree = dynamic_cast<TTree*>( infile->Get("DetectorTree") );

  //connect detector to the tree
  static ExitWinZEUS *det = 0x0;
  dtree->SetBranchAddress("ExitWinZEUS", &det);

  //ask for number of events
  Long64_t nev = dtree->GetEntries();
  cout << "Number of events: " << nev << endl;

  //nev = 12;

  //event loop
  for(Long64_t iev=0; iev<nev; iev++) {

    //get the event
    dtree->GetEntry(iev);

    //print information about exit window
    cout << "Gamma position (mm): " << det->GetX() << " " << det->GetY() << " " << det->GetZ() << endl;

  }//event loop






















}//reader

