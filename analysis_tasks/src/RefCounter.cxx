
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
#include "TH1D.h"

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
  fTrackTree->Branch("is_rec", &fRec, "is_rec/O");

  //track counter
  fCnt = new TH1D((fNam+"_hcnt").c_str(), (fNam+"_hcnt").c_str(), kMaxCnt-1, 1, kMaxCnt);

}//RefCounter

//_____________________________________________________________________________
void RefCounter::ProcessEvent() {

  //initialize the reference tracks in event
  fTracks.clear();

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

      //add the reference track for the event
      fTracks.push_back( Track() );
      Track& trk = fTracks.back();

      //track position
      trk.x = 0.5*(h1.x + h2.x);
      trk.y = 0.5*(h1.y + h2.y);

      //track angle
      trk.theta_x = TMath::ATan( (h2.x-h1.x)/(h2.z-h1.z) );
      trk.theta_y = TMath::ATan( (h2.y-h1.y)/(h2.z-h1.z) );

      //primary flag for the track
      trk.is_prim = h2.is_prim;

      //MC index and pdg for the track
      trk.itrk = h2.itrk;
      trk.pdg = h2.pdg;

    }//hit loop, plane 2
  }//hit loop, plane 1

}//ProcessEvent

//_____________________________________________________________________________
void RefCounter::FinishEvent() {

  //tracks loop
  for(const auto& i: fTracks) {

    //track position and angles
    fX = i.x;
    fY = i.y;
    fThetaX = i.theta_x;
    fThetaY = i.theta_y;

    //MC and reconstruction flags
    fPrim = i.is_prim;
    fRec = i.is_rec;

    //fill the track tree
    fTrackTree->Fill();

    //increment track counts
    fCnt->Fill( kAll );
    if(i.is_rec) fCnt->Fill( kRec );

  }//tracks loop

}//FinishEvent

//_____________________________________________________________________________
void RefCounter::WriteOutputs() {

  fTrackTree->Write();
  fCnt->Write();

  cout << "RefCounter " << fNam;
  cout << ", tracks: " << fCnt->GetBinContent(kAll);
  cout << ", reconstructed: " << fCnt->GetBinContent(kRec);
  if( fCnt->GetBinContent(kAll) > 0 ) {
    cout << ", efficiency: " << fCnt->GetBinContent(kRec)/fCnt->GetBinContent(kAll);
  }
  cout << endl;

}//WriteOutputs












