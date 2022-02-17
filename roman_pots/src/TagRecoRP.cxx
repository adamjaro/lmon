
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

}//Initialize

//_____________________________________________________________________________
void TagRecoRP::AddInput(Double_t x, Double_t y, Double_t theta_x, Double_t theta_y) {

  fHX->Fill(x);
  fHY->Fill(y);

  fHThetaX->Fill(theta_x);
  fHThetaY->Fill(theta_y);


}//AddInput

//_____________________________________________________________________________
void TagRecoRP::WriteOutput() {

  fHX->Write();
  fHY->Write();
  fHThetaX->Write();
  fHThetaY->Write();

}//WriteOutput

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























