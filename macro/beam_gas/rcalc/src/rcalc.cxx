
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
    hit_x(0), hit_y(0), hit_z(0), rmin(-1), zpos(0), rpos(0), en(0), pdg(0),
    nhits(0), phot_en(0), gen_pdg(0), gen_en(0) {

  inp = 0x0;
  outp = 0x0;

  cout << "Hi from rcalc" << endl;

}//

//_____________________________________________________________________________
rcalc::~rcalc() {

  cout << "~rcalc" << endl;

  if(outp) {
    htree->Write();
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
  for(int iev=0; iev<nev; iev++) {
    tree->GetEntry(iev);

    nhits = 0;

    //hit loop
    for(int ihit=0; ihit<hit_pdg->size(); ihit++) {

      nhits++;

      //hit radial position
      Double_t radius = TMath::Sqrt( hit_x->at(ihit)*hit_x->at(ihit) + hit_y->at(ihit)*hit_y->at(ihit) );

      //minimal hit radius if set
      if( rmin > 0. and radius < rmin ) continue;

      //hit output
      zpos = hit_z->at(ihit);
      rpos = radius;
      en = hit_en->at(ihit);
      pdg = hit_pdg->at(ihit);

      htree->Fill();

    }//hit loop

    //event with hits
    if(nhits <= 0) continue;

    //generated particles
    for(int imc=0; imc<gen_pdg->size(); imc++) {
      if( gen_pdg->at(imc) != 22 ) continue;

      phot_en = gen_en->at(imc);
    }

    //cout << nhits << " " << phot_en << endl;

    etree->Fill();

  }//event loop

  cout << "All events:       " << nev << endl;
  cout << "All hits:         " << htree->GetEntries() << endl;
  cout << "Events with hits: " << etree->GetEntries() << endl;

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

  tree->SetBranchAddress("gen_pdg", &gen_pdg);
  tree->SetBranchAddress("gen_en", &gen_en);

}//open_input

//_____________________________________________________________________________
void rcalc::create_output(std::string outfile) {

  outp = TFile::Open(outfile.c_str(), "recreate");

  //hit tree
  htree = new TTree("htree", "htree");
  htree->Branch("vtx_z", &vtx_z, "vtx_z/D");
  htree->Branch("zpos", &zpos, "zpos/D");
  htree->Branch("rpos", &rpos, "rpos/D");
  htree->Branch("en", &en, "en/D");
  htree->Branch("pdg", &pdg, "pdg/I");

  //event tree
  etree = new TTree("event", "event");
  etree->Branch("vtx_z", &vtx_z, "vtx_z/D");
  etree->Branch("nhits", &nhits, "nhits/I");
  etree->Branch("phot_en", &phot_en, "phot_en/D");

}//create_output



























