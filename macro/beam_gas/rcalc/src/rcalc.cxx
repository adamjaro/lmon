
//C++
#include <iostream>
#include <string.h>

//ROOT
#include "TFile.h"
#include "TTree.h"
#include "TMath.h"

//local classes
#include "rcalc.h"

using namespace std;

//_____________________________________________________________________________
rcalc::rcalc(): vtx_z(0), hit_pdg(0), hit_en(0), hit_x(0), hit_y(0), hit_z(0) {

  inp = 0x0;
  outp = 0x0;

  cout << "Hi from rcalc" << endl;

}//

//_____________________________________________________________________________
rcalc::~rcalc() {

  cout << "~rcalc" << endl;

  if(outp) {
    otree->Write();
    outp->Close();
  }

  if(inp) {
    inp->Close();
  }

}//~rcalc

//_____________________________________________________________________________
void rcalc::event_loop() {

  //number of events
  ULong64_t nev = tree->GetEntries();

  //event loop
  for(int iev=0; iev<nev; iev++) {
    tree->GetEntry(iev);

    //cout << vtx_z << endl;

    //if( hit_pdg->size() <= 0 ) continue;

    int nsel = 0;

    //hit loop
    for(int ihit=0; ihit<hit_pdg->size(); ihit++) {

      //photon hit
      if( hit_pdg->at(ihit) != 22 ) continue;
      nsel++;

      zpos = hit_z->at(ihit);
      rpos = TMath::Sqrt( hit_x->at(ihit)*hit_x->at(ihit) + hit_y->at(ihit)*hit_y->at(ihit) );

      //cout << hit_z->at(ihit) << " " << vtx_z << endl;
      //cout << TMath::Sqrt( hit_x->at(ihit)*hit_x->at(ihit) + hit_y->at(ihit)*hit_y->at(ihit) ) << endl;

    }//hit loop

    if( nsel <= 0 ) continue;

    otree->Fill();

  }//event loop


}//event_loop

//_____________________________________________________________________________
void rcalc::open_input(string infile) {

  inp = TFile::Open(infile.c_str());
  tree = dynamic_cast<TTree*>( inp->Get("DetectorTree") );

  tree->SetBranchAddress("vtx_z", &vtx_z);

  //tree->SetBranchAddress("beam_HitPdg", &hit_pdg);
  //tree->SetBranchAddress("beam_HitEn", &hit_en);
  //tree->SetBranchAddress("beam_HitX", &hit_x);
  //tree->SetBranchAddress("beam_HitY", &hit_y);
  //tree->SetBranchAddress("beam_HitZ", &hit_z);

  tree->SetBranchAddress("zplane_HitPdg", &hit_pdg);
  tree->SetBranchAddress("zplane_HitEn", &hit_en);
  tree->SetBranchAddress("zplane_HitX", &hit_x);
  tree->SetBranchAddress("zplane_HitY", &hit_y);
  tree->SetBranchAddress("zplane_HitZ", &hit_z);

  //cout << hit_pdg << endl;

}//open_input

//_____________________________________________________________________________
void rcalc::create_output(std::string outfile) {

  outp = TFile::Open(outfile.c_str(), "recreate");
  otree = new TTree("rtree", "rtree");

  otree->Branch("vtx_z", &vtx_z, "vtx_z/D");

  otree->Branch("zpos", &zpos, "zpos/D");
  otree->Branch("rpos", &rpos, "rpos/D");

}//create_output



























