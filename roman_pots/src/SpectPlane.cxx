
//_____________________________________________________________________________
//
// Counting plane for luminosity spectrometer
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

using namespace std;

//_____________________________________________________________________________
SpectPlane::SpectPlane(string nam, string geo_nam, TTree *tree, GeoParser *geo):
    fNam(nam), fEmin(0), fPdgSel(0), ltree(0x0) {

  fHits.ConnectInput(nam, tree);
  fHits.LocalFromGeo(geo_nam, geo);

}//SpectPlane

//_____________________________________________________________________________
bool SpectPlane::IsHit() {

  int nsel = 0;

  //hit loop
  for(int ihit=0; ihit<fHits.GetNHits(); ihit++) {

    ParticleCounterHits::CounterHit hit = fHits.GlobalToLocal( fHits.GetHit(ihit) );

    if( hit.en < fEmin ) continue;
    if( hit.pdg != fPdgSel ) continue;

    fX = hit.x;
    fY = hit.y;
    fZ = hit.z;
    fEn = hit.en;

    nsel++;

  }//hit loop

  if( nsel != 1 ) return false;

  if(ltree) ltree->Fill();

  return true;

}//IsHit

//_____________________________________________________________________________
void SpectPlane::CreateOutput() {

  //create output tree for the layer

  ltree = new TTree(fNam.c_str(), fNam.c_str());
  ltree->Branch("x", &fX, "x/D");
  ltree->Branch("y", &fY, "y/D");
  ltree->Branch("z", &fZ, "x/D");
  ltree->Branch("en", &fEn, "en/D");

}//CreateOutput

//_____________________________________________________________________________
void SpectPlane::WriteOutputs() {

  if(!ltree) return;

  cout << "Layer " << fNam << ": " << ltree->GetEntries() << endl;
  ltree->Write();

}//WriteOutputs

















