
//_____________________________________________________________________________
//
// Spectrometer detecting station
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>

//ROOT
#include "TTree.h"
#include "TMath.h"

//local classes
#include "GeoParser.h"
#include "SpectPlane.h"
#include "SpectDet.h"

using namespace std;

//_____________________________________________________________________________
SpectDet::SpectDet(std::string nam, string geo_nam, TTree *tree, GeoParser *geo):
    fNam(nam), fSTree(0x0) {

  fLay.push_back( new SpectPlane(nam+"_layA", geo_nam, tree, geo) );
  fLay.push_back( new SpectPlane(nam+"_layB", geo_nam, tree, geo) );
  fLay.push_back( new SpectPlane(nam+"_layC", geo_nam, tree, geo) );

  fCal.ConnectInput(fNam+"_cal", tree);

}//SpectDet

//_____________________________________________________________________________
bool SpectDet::IsHit() {

  fX = -9e9;
  fY = -9e9;
  fZ = -9e9;
  fThetaX = -9e9;
  fThetaY = -9e9;
  fCalE = -9e9;

  bool is_hit = true;

  //layers loop
  for(vector<SpectPlane*>::iterator ip = fLay.begin(); ip != fLay.end(); ip++) {

    is_hit *= (*ip)->IsHit();

  }//layers loop

  if( !is_hit ) return false;

  //layers for track position and angles
  SpectPlane *layA = fLay[0];
  SpectPlane *layC = fLay[2];

  //track position and angle
  fX = layA->GetX();
  fY = layA->GetY();
  fZ = layA->GetZ();
  fThetaX = GetTheta(layA->GetX(), layA->GetZ(), layC->GetX(), layC->GetZ());
  fThetaY = GetTheta(layA->GetY(), layA->GetZ(), layC->GetY(), layC->GetZ());

  //calorimeter deposited energy
  fCalE = 0.;
  fCal.LoadHits();
  for(unsigned long i=0; i<fCal.GetNhits(); i++) {
    fCalE += fCal.GetHit(i).en;
  }

  if(fSTree) fSTree->Fill();

  return true;

}//ProcessEvent

//_____________________________________________________________________________
void SpectDet::SetLayEmin(double emin) {

  //minimal energy for tracking layers

  for(vector<SpectPlane*>::iterator ip = fLay.begin(); ip != fLay.end(); ip++) {
    (*ip)->SetEmin(emin);
  }

}//SetLayEmin

//_____________________________________________________________________________
void SpectDet::SetLayPdg(int pdg) {

  //pdg selection for trackin layers

  for(vector<SpectPlane*>::iterator ip = fLay.begin(); ip != fLay.end(); ip++) {
    (*ip)->SetPdgSel(pdg);
  }

}//SetLayPdg

//_____________________________________________________________________________
void SpectDet::CreateOutput() {

  //output for the spectrometer
  fSTree = new TTree(fNam.c_str(), fNam.c_str());
  fSTree->Branch("x", &fX, "x/D");
  fSTree->Branch("y", &fY, "y/D");
  fSTree->Branch("z", &fZ, "z/D");
  fSTree->Branch("theta_x", &fThetaX, "theta_x/D");
  fSTree->Branch("theta_y", &fThetaY, "theta_y/D");
  fSTree->Branch("calE", &fCalE, "calE/D");

  //output for layers
  for_each(fLay.begin(), fLay.end(), mem_fun( &SpectPlane::CreateOutput ));

}//CreateOutput

//_____________________________________________________________________________
void SpectDet::WriteOutputs() {

  if(fSTree) fSTree->Write();

  for_each(fLay.begin(), fLay.end(), mem_fun( &SpectPlane::WriteOutputs ));

}//WriteOutputs

//_____________________________________________________________________________
Double_t SpectDet::GetTheta(Double_t xyA, Double_t zA, Double_t xyC, Double_t zC) {

  //track angle from two its points, mrad

  return 1e3*TMath::ATan( (xyC-xyA)/(zA-zC) );

}//GetTheta



















