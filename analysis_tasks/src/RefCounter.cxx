
//_____________________________________________________________________________
//
// Reference counter consisting of two planes placed along z
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
#include "TagCounterPlane.h"
#include "RefCounter.h"

using namespace std;

//_____________________________________________________________________________
RefCounter::RefCounter(string nam, TTree *tree, GeoParser *geo, TTree *otree):
    fNam(nam) {

  //planes for the counter
  fP1 = new TagCounterPlane(fNam+"_1", tree, geo); // plane 1 at lower z
  fP2 = new TagCounterPlane(fNam+"_2", tree, geo); // plane 2 at higher z

  //event quantities
  otree->Branch((fNam+"_ntrk").c_str(), &fNtrk, (fNam+"_ntrk/I").c_str());
  otree->Branch((fNam+"_ntrk_prim").c_str(), &fNtrkPrim, (fNam+"_ntrk_prim/I").c_str());

  //track output tree
  fTrackTree = new TTree(fNam.c_str(), fNam.c_str());
  fTrackTree->Branch("pos_x", &fX, "pos_x/D");
  fTrackTree->Branch("pos_y", &fY, "pos_y/D");
  fTrackTree->Branch("theta_x", &fThetaX, "theta_x/D");
  fTrackTree->Branch("theta_y", &fThetaY, "theta_y/D");
  fTrackTree->Branch("is_prim", &fPrim, "is_prim/O");

}//RefCounter

//_____________________________________________________________________________
void RefCounter::ProcessEvent() {

  //hits for the planes
  ParticleCounterHits& hits1 = fP1->GetHits();
  ParticleCounterHits& hits2 = fP2->GetHits();

  //reset the track counts
  fNtrk = 0;
  fNtrkPrim = 0;

  //hit loop, plane 1
  for(int ihit1=0; ihit1<hits1.GetNHits(); ihit1++) {
    ParticleCounterHits::CounterHit h1 = hits1.GetHit(ihit1);
    h1 = hits1.GlobalToLocal(h1);

    //hit loop, plane 2
    for(int ihit2=0; ihit2<hits2.GetNHits(); ihit2++) {
      ParticleCounterHits::CounterHit h2 = hits2.GetHit(ihit2);
      h2 = hits2.GlobalToLocal(h2);

      //matching track with plane 1
      if( h2.itrk != h1.itrk ) continue;

      //increment the track counts
      fNtrk++;
      if( h2.is_prim ) fNtrkPrim++;

      //cout << h1.x << " " << h1.y << " " << h1.z << " " << h1.itrk <<  " " << h2.itrk << " " << h1.is_prim << endl;

      //track position
      fX = 0.5*(h1.x + h2.x);
      fY = 0.5*(h1.y + h2.y);

      //track angle
      fThetaX = TMath::ATan( (h2.x-h1.x)/(h2.z-h1.z) );
      fThetaY = TMath::ATan( (h2.y-h1.y)/(h2.z-h1.z) );

      //primary flag for the track
      fPrim = h2.is_prim;

      //fill the track tree
      fTrackTree->Fill();

    }//hit loop, plane 2

  }//hit loop, plane 1



}//ProcessEvent

//_____________________________________________________________________________
void RefCounter::WriteOutputs() {

  fTrackTree->Write();

  cout << "RefCounter " << fNam << " tracks: " << fTrackTree->GetEntries() << endl;

}//WriteOutputs












