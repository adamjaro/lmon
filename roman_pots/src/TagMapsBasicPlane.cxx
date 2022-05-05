
//_____________________________________________________________________________
//
// Tagger station composed of MAPS basic planes
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
#include "TagMapsBasicPlane.h"

using namespace std;

//_____________________________________________________________________________
TagMapsBasicPlane::TagMapsBasicPlane(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree):
    fNam(nam), fEmin(0.4), fTree(0), fEvtTree(evt_tree), fNhit(0) {

  //connect the hits for the plane
  fHits.ConnectInput("lowQ2_"+fNam, tree);
  fHits.LocalFromGeo("vac_B2Q3", geo);

  //correct for local plane position inside its volume
  fHits.SetXPos( fHits.GetXPos() + geo->GetD("lowQ2_"+fNam, "xpos") );

}//TagMapsBasicPlane

//_____________________________________________________________________________
void TagMapsBasicPlane::LoadHits() {

  //load hits for current event in input tree
  fHits.LoadHits();
  fHits.GlobalToLocal();

}//LoadHits

//_____________________________________________________________________________
void TagMapsBasicPlane::ProcessEvent() {

  //process hits for current event

  fNhit = 0;

  //hits loop
  for(unsigned long ihit=0; ihit<fHits.GetNhits(); ihit++) {

    //get the hit
    const TrkMapsBasicHits::Hit& hit = fHits.GetHit(ihit);

    //energy threshold
    if( hit.en < fEmin ) continue;

    //set the outputs
    fNhit++;

    fX = hit.x;
    fY = hit.y;
    fZ = hit.z;
    fE = hit.en;

    fPdg = hit.pdg;
    fId = hit.itrk;

    //cout << fNam << ": " << hit.pdg << " " << hit.x << " " << hit.y << " " << hit.z << " " << hit.en << endl;

    //fill output for the layer
    if(fTree) fTree->Fill();

  }//hits loop

}//ProcessEvent

//_____________________________________________________________________________
void TagMapsBasicPlane::CreateOutput() {

  //output for the layer
  fTree = new TTree(fNam.c_str(), fNam.c_str());
  fTree->Branch("x", &fX, "x/D");
  fTree->Branch("y", &fY, "y/D");
  fTree->Branch("z", &fZ, "x/D");
  fTree->Branch("en", &fE, "en/D");
  fTree->Branch("pdg", &fPdg, "pdg/I");
  fTree->Branch("id", &fId, "id/I");

  //event tree
  fEvtTree->Branch((fNam+"_nhit").c_str(), &fNhit, (fNam+"_nhit/I").c_str());

}//CreateOutput

//_____________________________________________________________________________
void TagMapsBasicPlane::WriteOutputs() {

  if(!fTree) return;

  cout << "Plane " << fNam << ": " << fTree->GetEntries() << endl;
  fTree->Write();

}//WriteOutputs






















