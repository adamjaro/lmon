
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
#include "TMath.h"

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
  nhit = 0;

  //hit loop
  for(int ihit=0; ihit<fHits.GetNHits(); ihit++) {

    ParticleCounterHits::CounterHit hit = fHits.GetHit(ihit);
    if( hit.parentID != 0 ) continue;

    hit = fHits.GlobalToLocal(hit);
    fX = hit.x;
    fY = hit.y;
    fZ = hit.z;
    nhit++;

    //inner hit loop
    for(int jhit=ihit+1; jhit<fHits.GetNHits(); jhit++) {
      ParticleCounterHits::CounterHit hit2 = fHits.GetHit(jhit);
      if( hit2.parentID != 0 ) continue;
      hit2 = fHits.GlobalToLocal(hit2);

      fDx = TMath::Abs( hit.x-hit2.x );
      fDy = TMath::Abs( hit.y-hit2.y );
      fDxy = TMath::Sqrt( fDx*fDx + fDy*fDy );

      //cout << fNam << " " << fDx << " " << fDy << " " << fDxy << endl;
      pair_tree->Fill();

    }//inner hit loop

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
  ptree->Branch("z", &fZ, "x/D");

  pair_tree = new TTree((fNam+"_pairs").c_str(), (fNam+"_pairs").c_str());
  pair_tree->Branch("dx", &fDx, "dx/D");
  pair_tree->Branch("dy", &fDy, "dy/D");
  pair_tree->Branch("dxy", &fDxy, "dxy/D");

}//CreateOutput

//_____________________________________________________________________________
void TagCounterPlane::WriteOutputs() {

  if(!ptree) return;

  cout << "Plane " << fNam << ": " << ptree->GetEntries() << endl;
  ptree->Write();
  pair_tree->Write();

}//WriteOutputs






















