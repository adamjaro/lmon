
//_____________________________________________________________________________
//
// Counting plane for tagger station
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>

//ROOT
#include "TTree.h"

//Geant
#include "G4String.hh"

//local classes
#include "GeoParser.h"
#include "TagCounterPlane.h"

using namespace std;

//_____________________________________________________________________________
TagCounterPlane::TagCounterPlane(string nam, TTree *tree, GeoParser *geo):
    fNam(nam), ptree(0x0) {

  fHits.ConnectInput("lowQ2_"+fNam, tree);
  fHits.LocalFromGeo("vac_B2Q3", geo);

  //correct for local plane position inside its volume
  fHits.SetXPos( fHits.GetXPos() + geo->GetD("lowQ2_"+fNam, "xpos") );

}//TagCounterPlane

//_____________________________________________________________________________
bool TagCounterPlane::IsHit() {

  fX = -999; fY = -999; fZ = -999;
  int nhit = 0;

  //hit loop
  for(int ihit=0; ihit<fHits.GetNHits(); ihit++) {

    ParticleCounterHits::CounterHit hit = fHits.GetHit(ihit);
    if( hit.parentID != 0 ) continue;

    hit = fHits.GlobalToLocal(hit);
    fX = hit.x;
    fY = hit.y;
    fZ = hit.z;
    nhit++;
  }//hit loop

  if( nhit <= 0 ) return false;

  if(ptree) ptree->Fill();
  return true;

}//IsHit

//_____________________________________________________________________________
void TagCounterPlane::CreateOutput() {

  //create output tree for the plane

  ptree = new TTree(fNam.c_str(), fNam.c_str());
  ptree->Branch("x", &fX, "x/D");
  ptree->Branch("y", &fY, "y/D");
  ptree->Branch("z", &fZ, "Z/D");

}//CreateOutput

//_____________________________________________________________________________
void TagCounterPlane::WriteOutputs() {

  if(!ptree) return;

  cout << "Plane " << fNam << ": " << ptree->GetEntries() << endl;
  ptree->Write();

}//WriteOutputs






















