
//_____________________________________________________________________________
//
// Particle energy and polar theta and azimuthal phi angles
// are reconstructed out of a set of measured quantities
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>
#include <iostream>

//Boost
#include <boost/program_options.hpp>

//ROOT
#include "TTree.h"
#include "TH1D.h"
#include "TFile.h"

//local classes
#include "EThetaPhiReco.h"

using namespace std;
using namespace boost::program_options;

//_____________________________________________________________________________
EThetaPhiReco::EThetaPhiReco(string nam, options_description *opt):
    fNam(nam), fOpt(opt) {

}//EThetaPhiReco

//_____________________________________________________________________________
void EThetaPhiReco::MakeQuantity(string qnam, double conv) {

  //create a measured quantity

  fQuant.push_back( Quantity(qnam, conv) );

  //related program options
  AddOpt<int>("n"+qnam); // number of bins for the quantity
  AddOpt<double>(qnam+"min"); // minimal value
  AddOpt<double>(qnam+"max"); // maximal value

}//MakeQuantity

//_____________________________________________________________________________
void EThetaPhiReco::Initialize(variables_map *opt_map) {

  //initialization from the given program options

  //quantity loop
  for(vector<Quantity>::iterator i = fQuant.begin(); i != fQuant.end(); i++) {

    //distribution specification for the quantity
    Quantity& q = *i;
    int nbin = GetOpt<int>("n"+q.nam, opt_map);
    double hmin = GetOpt<double>(q.nam+"min", opt_map)*q.conv;
    double hmax = GetOpt<double>(q.nam+"max", opt_map)*q.conv;
    string hnam = fNam+"_h"+q.nam;

    //create the distribution for the quantity
    q.hist = new TH1D(hnam.c_str(), hnam.c_str(), nbin, hmin, hmax);

  }//quantity loop

}//Initialize

//_____________________________________________________________________________
void EThetaPhiReco::AddInput(Double_t *quant, Double_t en, Double_t theta, Double_t phi) {

  //add input particle

  //distributions in quantities
  for(unsigned int iq=0; iq<fQuant.size(); iq++) {
    fQuant[iq].hist->Fill( quant[iq] );
  }

  //linear index for the quantities
  ULong64_t idx = GetIdx(quant);

  //test for the range
  if( idx == 0 ) return;

  //link to the particle
  map<ULong64_t, Link>::iterator ilnk = fLinks.find(idx);

  //add the link if not present
  if( ilnk == fLinks.end() ) {
    ilnk = fLinks.insert( make_pair(idx, Link()) ).first;
  }

  //add particle input to the link
  Link& lnk = (*ilnk).second;
  lnk.AddParticle(en, theta, phi);

}//AddInput

//_____________________________________________________________________________
void EThetaPhiReco::Export() {

  //export to file

  //quantities
  TList lq;
  for(vector<Quantity>::iterator i = fQuant.begin(); i != fQuant.end(); i++) {
    lq.AddLast( (*i).hist );
  }

  lq.Write((fNam+"_quantities").c_str(), TObject::kSingleKey);

  //tree on links
  TTree link_tree((fNam+"_links").c_str(), (fNam+"_links").c_str());
  ULong64_t idx;
  Double_t en, theta, phi;
  Int_t ninp;
  link_tree.Branch("idx", &idx, "idx/l");
  link_tree.Branch("en", &en, "en/D");
  link_tree.Branch("theta", &theta, "theta/D");
  link_tree.Branch("phi", &phi, "phi/D");
  link_tree.Branch("ninp", &ninp, "ninp/I");

  //link loop
  for(map<ULong64_t, Link>::iterator i = fLinks.begin(); i != fLinks.end(); i++) {

    //link index
    idx = (*i).first;

    //link parameters
    Link& lnk = (*i).second;
    lnk.Evaluate();
    en = lnk.en;
    theta = lnk.theta;
    phi = lnk.phi;
    ninp = lnk.GetNinp();

    link_tree.Fill();

  }//link loop

  link_tree.Write();

}//Export

//_____________________________________________________________________________
void EThetaPhiReco::Import(TFile *in) {

  //import from file

  //quantities
  TList *lq = dynamic_cast<TList*>( in->Get((fNam+"_quantities").c_str()) );
  for(Int_t i=0; i<lq->GetEntries(); i++) {
    fQuant.push_back( Quantity(lq->At(i)->GetName()) );
    fQuant.back().hist = dynamic_cast<TH1D*>(lq->At(i));
  }

  //links
  TTree *link_tree = dynamic_cast<TTree*>( in->Get( (fNam+"_links").c_str() ) );
  ULong64_t idx;
  Double_t en, theta, phi;
  link_tree->SetBranchAddress("idx", &idx);
  link_tree->SetBranchAddress("en", &en);
  link_tree->SetBranchAddress("theta", &theta);
  link_tree->SetBranchAddress("phi", &phi);

  //links tree loop
  for(Long64_t i=0; i<link_tree->GetEntries(); i++) {
    link_tree->GetEntry(i);

    //create the link from input tree
    map<ULong64_t, Link>::iterator ilnk = fLinks.insert( make_pair(idx, Link()) ).first;

    //set the link
    Link& lnk = (*ilnk).second;
    lnk.en = en;
    lnk.theta = theta;
    lnk.phi = phi;

  }//links tree loop

}//Import

//_____________________________________________________________________________
void EThetaPhiReco::CreateRecoOutput() {

  //create output from the reconstruction

  fRecTree = new TTree((fNam+"_rec").c_str(), (fNam+"_rec").c_str());
  fRecTree->Branch("rec_E", &rec_E, "rec_E/D");
  fRecTree->Branch("rec_theta", &rec_theta, "rec_theta/D");
  fRecTree->Branch("rec_phi", &rec_phi, "rec_phi/D");

}//CreateRecoOutput

//_____________________________________________________________________________
void EThetaPhiReco::AddOutputBranch(string nam, Double_t *val) {

  //add a branch to the station output tree

  fRecTree->Branch(nam.c_str(), val, (nam+"/D").c_str());

}//AddOutputBranch

//_____________________________________________________________________________
void EThetaPhiReco::Reconstruct(Double_t *quant) {

  //run reconstruction for the measured quantities

  //link to the particle
  map<ULong64_t, Link>::iterator ilnk = fLinks.find( GetIdx(quant) );

  //test for the link
  if( ilnk == fLinks.end() ) return;

  //set the reconstructed particle
  Link& lnk = (*ilnk).second;
  rec_E = lnk.en;
  rec_theta = lnk.theta;
  rec_phi = lnk.phi;

  fRecTree->Fill();

}//Reconstruct

//_____________________________________________________________________________
ULong64_t EThetaPhiReco::GetIdx(Double_t *quant) {

  //linear index for the quantities

  ULong64_t idx = 0;

  //quantity loop
  for(unsigned int iq=0; iq<fQuant.size(); iq++) {

    //test for the range
    Int_t ibin = fQuant[iq].hist->FindBin( quant[iq] );
    if( ibin < 1 or ibin > fQuant[iq].hist->GetNbinsX() ) return 0;

    //segment base for the quantity
    ULong64_t seg = 1;
    for(unsigned int is=0; is<iq; is++) {
      seg *= ULong64_t( fQuant[is].hist->GetNbinsX() );
    }

    idx += ULong64_t(ibin)*seg;

  }//quantity loop

  return idx;

}//GetIdx

//_____________________________________________________________________________
template<typename T> void EThetaPhiReco::AddOpt(string onam) {

  fOpt->add_options()
    ((fNam+"."+onam).c_str(), value<T>(), (fNam+"."+onam).c_str())
  ;

}//AddOpt

//_____________________________________________________________________________
template<typename T> T EThetaPhiReco::GetOpt(string onam, variables_map *opt_map) {

  return opt_map->at( fNam+"."+onam ).as<T>();

}//GetOpt

//_____________________________________________________________________________
void EThetaPhiReco::Link::AddParticle(double e, double t, double p) {

  //add particle for the link

  fEn.push_back(e);
  fTheta.push_back(t);
  fPhi.push_back(p);

}//Link::AddParticle

//_____________________________________________________________________________
void EThetaPhiReco::Link::Evaluate() {

  //assign particle energy and angles from inputs for a given link

  if( fEn.size() > 1 ) {

    en = GetMean(fEn);
    theta = GetMean(fTheta);
    phi = GetMean(fPhi);

  } else {

    en = fEn[0];
    theta = fTheta[0];
    phi = fPhi[0];
  }

}//Link::Evaluate

//_____________________________________________________________________________
Double_t EThetaPhiReco::Link::GetMean(std::vector<double>& v) {

  //mean for a set of values

  Double_t nx = Double_t(v.size());

  Double_t sum = 0.;
  for(unsigned int i=0; i<v.size(); i++) {
    sum += v[i];
  }

  return sum/nx;

}//GetMean









