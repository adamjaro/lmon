
//_____________________________________________________________________________
//
// Reconstruction for Roman Pot tagger station
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
#include "TMath.h"

//Geant
//#include "G4String.hh"

//local classes
#include "TagRecoRP.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
TagRecoRP::TagRecoRP(string nam, program_options::options_description *opt):
    fNam(nam), fHX(0x0), fHY(0x0), fHThetaX(0x0), fHThetaY(0x0) {

  AddOpt<int>("nx", opt);
  AddOpt<double>("xmin", opt);
  AddOpt<double>("xmax", opt);
  AddOpt<int>("ny", opt);
  AddOpt<double>("ymin", opt);
  AddOpt<double>("ymax", opt);

  AddOpt<int>("ntx", opt);
  AddOpt<double>("txmin", opt);
  AddOpt<double>("txmax", opt);
  AddOpt<int>("nty", opt);
  AddOpt<double>("tymin", opt);
  AddOpt<double>("tymax", opt);

}//TagRecoRP

//_____________________________________________________________________________
void TagRecoRP::Initialize(program_options::variables_map *opt_map) {

  //initialization from the given configuration

  //segmentation in x, mm
  int nx = GetOpt<int>("nx", opt_map);
  double xmin = GetOpt<double>("xmin", opt_map);
  double xmax = GetOpt<double>("xmax", opt_map);
  fHX = new TH1D((fNam+"_hx").c_str(), (fNam+"_hx").c_str(), nx, xmin, xmax);

  //segmentation in y, mm
  int ny = GetOpt<int>("ny", opt_map);
  double ymin = GetOpt<double>("ymin", opt_map);
  double ymax = GetOpt<double>("ymax", opt_map);
  fHY = new TH1D((fNam+"_hy").c_str(), (fNam+"_hy").c_str(), ny, ymin, ymax);

  //segmentation in theta_x, rad
  int ntx = GetOpt<int>("ntx", opt_map);
  double txmin = GetOpt<double>("txmin", opt_map)*1e-3; // to mrad
  double txmax = GetOpt<double>("txmax", opt_map)*1e-3;
  fHThetaX = new TH1D((fNam+"_htheta_x").c_str(), (fNam+"_htheta_x").c_str(), ntx, txmin, txmax);

  //segmentation in theta_y, rad
  int nty = GetOpt<int>("nty", opt_map);
  double tymin = GetOpt<double>("tymin", opt_map)*1e-3; // to mrad
  double tymax = GetOpt<double>("tymax", opt_map)*1e-3;
  fHThetaY = new TH1D((fNam+"_htheta_y").c_str(), (fNam+"_htheta_y").c_str(), nty, tymin, tymax);

  //links to electrons
  //x
  for(int ix=1; ix<fHX->GetNbinsX()+1; ix++) {
    cout << fNam << ", creating link: " << ix << endl;
    //y
    for(int iy=1; iy<fHY->GetNbinsX()+1; iy++) {
      //theta_x
      for(int itx=1; itx<fHThetaX->GetNbinsX()+1; itx++) {
        //theta_y
        for(int ity=1; ity<fHThetaY->GetNbinsX()+1; ity++) {

          fLinks.insert( make_pair(vector<int>({ix, iy, itx, ity}), Link()) );

        }//theta_y
      }//theta_x
    }//y
  }//x

}//Initialize

//_____________________________________________________________________________
void TagRecoRP::Import(TFile *in) {

  //import from input file

  //segmentation
  fHX = dynamic_cast<TH1D*>( in->Get( (fNam+"_hx").c_str() ) );
  fHY = dynamic_cast<TH1D*>( in->Get( (fNam+"_hy").c_str() ) );
  fHThetaX = dynamic_cast<TH1D*>( in->Get( (fNam+"_htheta_x").c_str() ) );
  fHThetaY = dynamic_cast<TH1D*>( in->Get( (fNam+"_htheta_y").c_str() ) );

  //links
  TTree *link_tree = dynamic_cast<TTree*>( in->Get( (fNam+"_link_tree").c_str() ) );
  Int_t ix, iy, itx, ity;
  Double_t en, theta, phi;
  link_tree->SetBranchAddress("ix", &ix);
  link_tree->SetBranchAddress("iy", &iy);
  link_tree->SetBranchAddress("itx", &itx);
  link_tree->SetBranchAddress("ity", &ity);
  link_tree->SetBranchAddress("en", &en);
  link_tree->SetBranchAddress("theta", &theta);
  link_tree->SetBranchAddress("phi", &phi);

  //links tree loop
  for(Long64_t i=0; i<link_tree->GetEntries(); i++) {
    link_tree->GetEntry(i);

    //create the link from input tree
    map<vector<int>, Link>::iterator ilnk = fLinks.insert( make_pair(vector<int>({ix, iy, itx, ity}), Link()) ).first;

    //set the link
    Link& lnk = (*ilnk).second;
    lnk.en = en;
    lnk.theta = theta;
    lnk.phi = phi;

  }//links tree loop

}//Import

//_____________________________________________________________________________
void TagRecoRP::AddInput(Double_t x, Double_t y, Double_t theta_x, Double_t theta_y, Double_t en, Double_t theta, Double_t phi) {

  fHX->Fill(x);
  fHY->Fill(y);

  fHThetaX->Fill(theta_x);
  fHThetaY->Fill(theta_y);

  int ix = fHX->FindBin(x);
  int iy = fHY->FindBin(y);
  int itx = fHThetaX->FindBin(theta_x);
  int ity = fHThetaY->FindBin(theta_y);

  map<vector<int>, Link>::iterator ilnk = fLinks.find( vector<int>{ix, iy, itx, ity} );
  if( ilnk == fLinks.end() ) return;

  Link& lnk = (*ilnk).second;
  lnk.AddElectron(en, theta, phi);

}//AddInput

//_____________________________________________________________________________
void TagRecoRP::Export() {

  //segmentation in tagger quantities
  fHX->Write();
  fHY->Write();
  fHThetaX->Write();
  fHThetaY->Write();

  //tree on links
  TTree link_tree((fNam+"_link_tree").c_str(), (fNam+"_link_tree").c_str());
  Int_t ix, iy, itx, ity;
  Double_t en, theta, phi;
  Int_t ninp;
  link_tree.Branch("ix", &ix, "ix/I");
  link_tree.Branch("iy", &iy, "iy/I");
  link_tree.Branch("itx", &itx, "itx/I");
  link_tree.Branch("ity", &ity, "ity/I");
  link_tree.Branch("en", &en, "en/D");
  link_tree.Branch("theta", &theta, "theta/D");
  link_tree.Branch("phi", &phi, "phi/D");
  link_tree.Branch("ninp", &ninp, "ninp/I");

  //links loop
  for(map<vector<int>, Link>::iterator i = fLinks.begin(); i != fLinks.end(); i++) {

    //valid links only
    Link& lnk = (*i).second;
    if( lnk.GetNinp() == 0 ) continue;

    //link parameters
    lnk.Evaluate();
    en = lnk.en;
    theta = lnk.theta;
    phi = lnk.phi;
    ninp = lnk.GetNinp();

    //link indices
    const vector<int>& idx = (*i).first;
    ix = idx[0];
    iy = idx[1];
    itx = idx[2];
    ity = idx[3];

    link_tree.Fill();

  }//links loop

  link_tree.Write();

}//Export

//_____________________________________________________________________________
void TagRecoRP::CreateRecoOutput() {

  //create output from the reconstruction

  fRecTree = new TTree((fNam+"_rec").c_str(), (fNam+"_rec").c_str());
  fRecTree->Branch("rec_el_E", &rec_el_E, "rec_el_E/D");
  fRecTree->Branch("rec_el_theta", &rec_el_theta, "rec_el_theta/D");
  fRecTree->Branch("rec_el_phi", &rec_el_phi, "rec_el_phi/D");
  fRecTree->Branch("rec_Q2", &rec_Q2, "rec_Q2/D");

}//CreateRecoOutput

//_____________________________________________________________________________
void TagRecoRP::AddOutputBranch(string nam, Double_t *val) {

  //add a branch to the station output tree

  fRecTree->Branch(nam.c_str(), val, (nam+"/D").c_str());

}//AddOutputBranch

//_____________________________________________________________________________
bool TagRecoRP::Reconstruct(Double_t x, Double_t y, Double_t theta_x, Double_t theta_y) {

  int ix = fHX->FindBin(x);
  int iy = fHY->FindBin(y);
  int itx = fHThetaX->FindBin(theta_x);
  int ity = fHThetaY->FindBin(theta_y);

  map<vector<int>, Link>::iterator ilnk = fLinks.find( vector<int>{ix, iy, itx, ity} );
  if( ilnk == fLinks.end() ) return false;

  Link& lnk = (*ilnk).second;

  //cout << lnk.en << " " << TMath::Pi()-lnk.theta << " " << lnk.phi << endl;

  //cout << lnk.en << " " << ((TMath::Pi())-lnk.theta)*1e3 << " " << lnk.phi << endl;

  //set the reconstructed electron
  rec_el_E = lnk.en;
  rec_el_theta = lnk.theta;
  rec_el_phi = lnk.phi;

  //calculate the Q^2
  rec_Q2 = 2.*18*rec_el_E*(1. - TMath::Cos(TMath::Pi()-rec_el_theta));

  //cout << TMath::Log10(rec_Q2) << endl;

  fRecTree->Fill();

  return true;

}//Reconstruct

//_____________________________________________________________________________
template<typename T>  void TagRecoRP::AddOpt(std::string onam, program_options::options_description *opt) {

  opt->add_options()
    ((fNam+"."+onam).c_str(), program_options::value<T>(), (fNam+"."+onam).c_str())
  ;

}//AddOpt

//_____________________________________________________________________________
template<typename T> T TagRecoRP::GetOpt(std::string onam, boost::program_options::variables_map *opt_map) {

  return opt_map->at( fNam+"."+onam ).as<T>();

}//GetOpt

//_____________________________________________________________________________
void TagRecoRP::Link::AddElectron(double e, double t, double p) {

  //add electron for the link

  fEn.push_back(e);
  fTheta.push_back(t);
  fPhi.push_back(p);

}//Link::AddElectron

//_____________________________________________________________________________
void TagRecoRP::Link::Evaluate() {

  //assign electron kinematics from inputs for a given link

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
Double_t TagRecoRP::Link::GetMean(std::vector<double>& v) {

  //mean for a set of values

  Double_t nx = Double_t(v.size());

  Double_t sum = 0.;
  for(unsigned int i=0; i<v.size(); i++) {
    sum += v[i];
  }

  return sum/nx;

}//GetMean













