
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
rcalc::rcalc(std::string nam): det_name(nam), vtx_z(0), hit_pdg(0), hit_en(0),
    hit_x(0), hit_y(0), hit_z(0), rmin(-1) {

  inp = 0x0;
  outp = 0x0;

  cout << "Hi from rcalc" << endl;

}//

//_____________________________________________________________________________
rcalc::~rcalc() {

  cout << "~rcalc" << endl;

  if(outp) {
    ptree->Write();
    etree->Write();
    outp->Close();
  }

  if(inp) {
    inp->Close();
  }

}//~rcalc

//_____________________________________________________________________________
void rcalc::event_loop(int n) {

  //number of events
  ULong64_t nev = tree->GetEntries();
  if( n >= 0 ) {
    nev = n;
  }

  //event loop
  ULong64_t nall = 0;
  ULong64_t nhit_all = 0;
  for(int iev=0; iev<nev; iev++) {
    tree->GetEntry(iev);

    //cout << vtx_z << endl;

    //if( vtx_z < 5000. ) continue;

    nall++;

    //if( hit_pdg->size() <= 0 ) continue;

    int nphot = 0;
    int nel = 0;

    //hit loop
    for(int ihit=0; ihit<hit_pdg->size(); ihit++) {
      nhit_all++;

      //hit radial position
      Double_t radius = TMath::Sqrt( hit_x->at(ihit)*hit_x->at(ihit) + hit_y->at(ihit)*hit_y->at(ihit) );

      //minimal hit radius if set
      if( rmin > 0. and radius < rmin ) continue;

      //photon or electron hit
      if( hit_pdg->at(ihit) == 22 ) {
        nphot++;

        phot_zpos = hit_z->at(ihit);
        phot_rpos = TMath::Sqrt( hit_x->at(ihit)*hit_x->at(ihit) + hit_y->at(ihit)*hit_y->at(ihit) );
        phot_en = hit_en->at(ihit);
      }
      if( hit_pdg->at(ihit) == 11 ) {
        nel++;

        el_zpos = hit_z->at(ihit);
        el_rpos = TMath::Sqrt( hit_x->at(ihit)*hit_x->at(ihit) + hit_y->at(ihit)*hit_y->at(ihit) );
        el_en = hit_en->at(ihit);
      }

      //cout << hit_z->at(ihit) << " " << vtx_z << endl;
      //cout << TMath::Sqrt( hit_x->at(ihit)*hit_x->at(ihit) + hit_y->at(ihit)*hit_y->at(ihit) ) << endl;

    }//hit loop

    if( nphot > 0 ) ptree->Fill();
    if( nel > 0 ) etree->Fill();

  }//event loop

  cout << "All events:    " << nall << endl;
  cout << "All hits:      " << nhit_all << endl;
  cout << "Photon hits:   " << ptree->GetEntries() << endl;
  cout << "Electron hits: " << etree->GetEntries() << endl;

}//event_loop

//_____________________________________________________________________________
void rcalc::open_input(string infile) {

  inp = TFile::Open(infile.c_str());
  tree = dynamic_cast<TTree*>( inp->Get("DetectorTree") );

  tree->SetBranchAddress("vtx_z", &vtx_z);

  tree->SetBranchAddress((det_name+"_HitPdg").c_str(), &hit_pdg);
  tree->SetBranchAddress((det_name+"_HitEn").c_str(), &hit_en);
  tree->SetBranchAddress((det_name+"_HitX").c_str(), &hit_x);
  tree->SetBranchAddress((det_name+"_HitY").c_str(), &hit_y);
  tree->SetBranchAddress((det_name+"_HitZ").c_str(), &hit_z);

  //cout << hit_pdg << endl;

}//open_input

//_____________________________________________________________________________
void rcalc::create_output(std::string outfile) {

  outp = TFile::Open(outfile.c_str(), "recreate");
  ptree = new TTree("ptree", "ptree");
  etree = new TTree("etree", "etree");

  ptree->Branch("vtx_z", &vtx_z, "vtx_z/D");
  etree->Branch("vtx_z", &vtx_z, "vtx_z/D");

  ptree->Branch("zpos", &phot_zpos, "zpos/D");
  ptree->Branch("rpos", &phot_rpos, "rpos/D");
  ptree->Branch("en", &phot_en, "en/D");

  etree->Branch("zpos", &el_zpos, "zpos/D");
  etree->Branch("rpos", &el_rpos, "rpos/D");
  etree->Branch("en", &el_en, "en/D");

}//create_output



























