
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
    fNam(nam), fEmin(0.4), fChi2ndfMax(4), fEvtTree(evt_tree) {

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

          //track parameters in x and y
          MakeTrack(x, fPosX, fSlopeX, fThetaX, fChi2X);
          MakeTrack(y, fPosY, fSlopeY, fThetaY, fChi2Y);

          //maximal tracks reduced chi2
          if( fChi2X > 2.*fChi2ndfMax ) continue; // 2 degrees of freedom
          if( fChi2Y > 2.*fChi2ndfMax ) continue; // 2 degrees of freedom

          //track for primary particle
          fPrim = c1.is_prim and c2.is_prim and c3.is_prim and c4.is_prim;

          fTrkTree->Fill();

          fNtrk++;
          if( fPrim ) fNtrkPrim++;

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
bool TagMapsBasic::SelectHit(const TrkMapsBasicHits::Hit& hit) {

  //hit selection

  //energy threshold
  if( hit.en < fEmin ) return false;

  return true;

}//SelectHit

//_____________________________________________________________________________
void TagMapsBasic::CreateOutput() {

  //create output for individual planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::CreateOutput ));

  //track tree for the tagger detector
  fTrkTree = new TTree((fNam+"_tracks").c_str(), (fNam+"_tracks").c_str());
  fTrkTree->Branch("pos_x", &fPosX, "pos_x/D");
  fTrkTree->Branch("pos_y", &fPosY, "pos_y/D");
  fTrkTree->Branch("slope_x", &fSlopeX, "slope_x/D");
  fTrkTree->Branch("slope_y", &fSlopeY, "slope_y/D");
  fTrkTree->Branch("theta_x", &fThetaX, "theta_x/D");
  fTrkTree->Branch("theta_y", &fThetaY, "theta_y/D");
  fTrkTree->Branch("chi2_x", &fChi2X, "chi2_x/D");
  fTrkTree->Branch("chi2_y", &fChi2Y, "chi2_y/D");
  fTrkTree->Branch("is_prim", &fPrim, "is_prim/O");

  //event quantities
  fEvtTree->Branch((fNam+"_ntrk").c_str(), &fNtrk, (fNam+"_ntrk/I").c_str());
  fEvtTree->Branch((fNam+"_ntrk_prim").c_str(), &fNtrkPrim, (fNam+"_ntrk_prim/I").c_str());

}//CreateOutput

//_____________________________________________________________________________
void TagMapsBasic::WriteOutputs() {

  //write outputs for the planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::WriteOutputs ));

  cout << "Tagger " << fNam << ", tracks: " << fTrkTree->GetEntries() << endl;

  fTrkTree->Write();

}//WriteOutputs

















