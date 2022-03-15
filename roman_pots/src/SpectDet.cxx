
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

//local classes
#include "GeoParser.h"
#include "SpectPlane.h"
#include "SpectDet.h"

using namespace std;

//_____________________________________________________________________________
SpectDet::SpectDet(std::string nam, string geo_nam, TTree *tree, GeoParser *geo) {

  fLay.push_back( new SpectPlane(nam+"_layA", geo_nam, tree, geo) );
  fLay.push_back( new SpectPlane(nam+"_layB", geo_nam, tree, geo) );
  fLay.push_back( new SpectPlane(nam+"_layC", geo_nam, tree, geo) );


}//SpectDet

//_____________________________________________________________________________
void SpectDet::ProcessEvent() {

  //layers loop
  for(vector<SpectPlane*>::iterator ip = fLay.begin(); ip != fLay.end(); ip++) {

    (*ip)->IsHit();

  }//layers loop

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

  for_each(fLay.begin(), fLay.end(), mem_fun( &SpectPlane::CreateOutput ));

}//CreateOutput

//_____________________________________________________________________________
void SpectDet::WriteOutputs() {

  for_each(fLay.begin(), fLay.end(), mem_fun( &SpectPlane::WriteOutputs ));

}//WriteOutputs





















