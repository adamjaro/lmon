
//_____________________________________________________________________________
//
// Tagger station composed of MAPS basic planes, tracking implementation
// follows Nucl.Instrum.Meth. 203 (1982) 291-297
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
#include "TagMapsBasicPlane.h"
#include "TagMapsBasic.h"

using namespace std;

//_____________________________________________________________________________
TagMapsBasic::TagMapsBasic(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree):
    fNam(nam), fChi2ndfMax(4), fEvtTree(evt_tree) {

  //planes for the station, 1 - 4
  fPlanes.push_back( new TagMapsBasicPlane(fNam+"_1", tree, geo, evt_tree) );
  fPlanes.push_back( new TagMapsBasicPlane(fNam+"_2", tree, geo, evt_tree) );
  fPlanes.push_back( new TagMapsBasicPlane(fNam+"_3", tree, geo, evt_tree) );
  fPlanes.push_back( new TagMapsBasicPlane(fNam+"_4", tree, geo, evt_tree) );

  //plane spacing, mm
  fL = geo->GetD("lowQ2_"+fNam+"_2", "zpos") - geo->GetD("lowQ2_"+fNam+"_1", "zpos");
  //cout << "L: " << fL << endl;

  //local z positions for planes, mm
  fZ[0] = (-3./2)*fL;
  fZ[1] = (-1./2)*fL;
  fZ[2] = (1./2)*fL;
  fZ[3] = (3./2)*fL;

  //middle z position for hits in local frame
  //G4double zmid = ( geo->GetD("lowQ2_"+fNam+"_4", "zpos") + geo->GetD("lowQ2_"+fNam+"_1", "zpos") )/2;

  //set z in planes to local frame
  //for(unsigned long i = 0; i < fPlanes.size(); i++) {
  //  fPlanes[i]->GetHits().SetZPos( fPlanes[i]->GetHits().GetZPos() + zmid );
  //}

}//TagMapsBasic

//_____________________________________________________________________________
void TagMapsBasic::ProcessEvent() {

  //initialize the event tracks
  fTracks.clear();

  //load hits for individual planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::ProcessEvent ));

  //clusters in planes
  const vector<TagMapsBasicPlane::Cluster>& cls1 = fPlanes[0]->GetClusters();
  const vector<TagMapsBasicPlane::Cluster>& cls2 = fPlanes[1]->GetClusters();
  const vector<TagMapsBasicPlane::Cluster>& cls3 = fPlanes[2]->GetClusters();
  const vector<TagMapsBasicPlane::Cluster>& cls4 = fPlanes[3]->GetClusters();

  //number of tracks per event
  fNtrk = 0;
  fNtrkPrim = 0;

  //plane 1
  for(unsigned long i1=0; i1<cls1.size(); i1++) {
    const TagMapsBasicPlane::Cluster& c1 = cls1[i1];

    //plane 2
    for(unsigned long i2=0; i2<cls2.size(); i2++) {
      const TagMapsBasicPlane::Cluster& c2 = cls2[i2];

      //plane 3
      for(unsigned long i3=0; i3<cls3.size(); i3++) {
        const TagMapsBasicPlane::Cluster& c3 = cls3[i3];

        //plane 4
        for(unsigned long i4=0; i4<cls4.size(); i4++) {
          const TagMapsBasicPlane::Cluster& c4 = cls4[i4];

          //make the track from the clusters

          //track points in x and y
          Double_t x[] = {c1.x, c2.x, c3.x, c4.x};
          Double_t y[] = {c1.y, c2.y, c3.y, c4.y};

          //track parameters in x and y for the track candidate
          Track init_trk;
          MakeTrack(x, init_trk.x, init_trk.slope_x, init_trk.theta_x, init_trk.chi2_x);
          MakeTrack(y, init_trk.y, init_trk.slope_y, init_trk.theta_y, init_trk.chi2_y);

          //maximal tracks reduced chi2
          if( init_trk.chi2_x > 2.*fChi2ndfMax ) continue; // 2 degrees of freedom
          if( init_trk.chi2_y > 2.*fChi2ndfMax ) continue; // 2 degrees of freedom

          //track is selected, add it for the event
          fTracks.push_back( init_trk );
          Track& trk = fTracks.back();

          //track for primary particle
          trk.is_prim = c1.is_prim and c2.is_prim and c3.is_prim and c4.is_prim;

          //MC particle corresponding to the track, set for all clusters from the same MC particle
          if( (c1.itrk == c2.itrk) and (c2.itrk == c3.itrk) and (c3.itrk == c4.itrk) ) {

            trk.itrk = c1.itrk;
            trk.pdg = c1.pdg;
          }

          //increment event quantities
          fNtrk++;
          if( trk.is_prim ) fNtrkPrim++;

        }//plane 4
      }//plane 3
    }//plane 2
  }//plane 1

}//ProcessEvent

//_____________________________________________________________________________
void TagMapsBasic::MakeTrack(Double_t *x, Double_t& pos, Double_t& slope, Double_t& theta, Double_t& chi2) {

  //track position (mm) and slope
  pos = (x[0]+x[1]+x[2]+x[3])/4.;

  slope = (-3*x[0]-x[1]+x[2]+3*x[3])/(10*fL);

  //angle, rad
  theta = TMath::ATan(slope);

  //chi^2
  chi2 = 0;
  for(int i=0; i<4; i++) {
    chi2 += (pos + slope*fZ[i] - x[i])*(pos + slope*fZ[i] - x[i]);
  }

  //cout << pos << " " << slope << " " << theta << " " << chi2 << endl;

}//MakeTrack

//_____________________________________________________________________________
void TagMapsBasic::FinishEvent() {

  //set output tree for tracks

  //counter for associated tracks in event
  fNtrkAssociated = 0;

  //tracks loop
  for(auto it = fTracks.begin(); it != fTracks.end(); it++) {

    //set the output track and fill the tree
    fOutTrk = *it;
    if( fOutTrk.is_associate ) fNtrkAssociated++;

    fTrkTree->Fill();

  } //tracks loop

}//FinishEvent

//_____________________________________________________________________________
void TagMapsBasic::CreateOutput() {

  //create output for individual planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::CreateOutput ));

  //track tree for the tagger detector
  fTrkTree = new TTree((fNam+"_tracks").c_str(), (fNam+"_tracks").c_str());
  fTrkTree->Branch("pos_x", &fOutTrk.x, "pos_x/D");
  fTrkTree->Branch("pos_y", &fOutTrk.y, "pos_y/D");
  fTrkTree->Branch("slope_x", &fOutTrk.slope_x, "slope_x/D");
  fTrkTree->Branch("slope_y", &fOutTrk.slope_y, "slope_y/D");
  fTrkTree->Branch("theta_x", &fOutTrk.theta_x, "theta_x/D");
  fTrkTree->Branch("theta_y", &fOutTrk.theta_y, "theta_y/D");
  fTrkTree->Branch("chi2_x", &fOutTrk.chi2_x, "chi2_x/D");
  fTrkTree->Branch("chi2_y", &fOutTrk.chi2_y, "chi2_y/D");
  fTrkTree->Branch("is_prim", &fOutTrk.is_prim, "is_prim/O");
  fTrkTree->Branch("is_associate", &fOutTrk.is_associate, "is_associate/O");

  //event quantities
  fEvtTree->Branch((fNam+"_ntrk").c_str(), &fNtrk, (fNam+"_ntrk/I").c_str());
  fEvtTree->Branch((fNam+"_ntrk_prim").c_str(), &fNtrkPrim, (fNam+"_ntrk_prim/I").c_str());
  fEvtTree->Branch((fNam+"_ntrk_associate").c_str(), &fNtrkAssociated, (fNam+"_ntrk_associate/I").c_str());

}//CreateOutput

//_____________________________________________________________________________
void TagMapsBasic::AddTrackBranch(string nam, Double_t *val) {

  //add a branch to the station output tree

  fTrkTree->Branch(nam.c_str(), val, (nam+"/D").c_str());

}//AddTrackBranch

//_____________________________________________________________________________
void TagMapsBasic::WriteOutputs() {

  //write outputs for the planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::WriteOutputs ));

  cout << "Tagger " << fNam << ", tracks: " << fTrkTree->GetEntries() << endl;

  fTrkTree->Write();

}//WriteOutputs

















