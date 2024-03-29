
//_____________________________________________________________________________
//
// Tagger station composed of MAPS basic planes, tracking implementation
// follows Nucl.Instrum.Meth. 203 (1982) 291-297
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>
#include <unordered_set>

//ROOT
#include "TTree.h"
#include "TMath.h"

//Geant
#include "G4String.hh"
#include "G4ios.hh"

//local classes
#include "GeoParser.h"
#include "TagMapsBasic.h"

using namespace std;

//_____________________________________________________________________________
TagMapsBasic::TagMapsBasic(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree):
    fNam(nam), fChi2ndfMax(0.5), fEvtTree(evt_tree), fAllTrkSig(0) {

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

  //G4cout << "TagMapsBasic::ProcessEvent, " << fNam << G4endl;

  //initialize the event tracks
  fTracks.clear();

  //load hits and make clusters for individual planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fn( &TagMapsBasicPlane::ProcessEvent ));

  //clusters in planes
  vector<TagMapsBasicPlane::Cluster>& cls1 = fPlanes[0]->GetClusters();
  vector<TagMapsBasicPlane::Cluster>& cls2 = fPlanes[1]->GetClusters();
  vector<TagMapsBasicPlane::Cluster>& cls3 = fPlanes[2]->GetClusters();
  vector<TagMapsBasicPlane::Cluster>& cls4 = fPlanes[3]->GetClusters();

  //number of tracks per event
  fNtrk = 0;
  fNtrkPrim = 0;

  //plane 1
  for(unsigned long i1=0; i1<cls1.size(); i1++) {
    TagMapsBasicPlane::Cluster& c1 = cls1[i1];
    c1.iplane = 1;
    if( !c1.stat ) continue;

    //plane 2
    for(unsigned long i2=0; i2<cls2.size(); i2++) {
      TagMapsBasicPlane::Cluster& c2 = cls2[i2];
      c2.iplane = 2;
      if( !c2.stat ) continue;

      //plane 3
      for(unsigned long i3=0; i3<cls3.size(); i3++) {
        TagMapsBasicPlane::Cluster& c3 = cls3[i3];
        c3.iplane = 3;
        if( !c3.stat ) continue;

        //plane 4
        for(unsigned long i4=0; i4<cls4.size(); i4++) {
          TagMapsBasicPlane::Cluster& c4 = cls4[i4];
          c4.iplane = 4;
          if( !c4.stat ) continue;

          //make the track from the clusters

          //track points in x and y
          Double_t x[] = {c1.x, c2.x, c3.x, c4.x};
          Double_t y[] = {c1.y, c2.y, c3.y, c4.y};

          //track parameters in x and y for the track candidate
          Track init_trk;
          MakeTrack(x, init_trk.x, init_trk.slope_x, init_trk.theta_x, init_trk.chi2_x);
          MakeTrack(y, init_trk.y, init_trk.slope_y, init_trk.theta_y, init_trk.chi2_y);

          //maximal tracks reduced chi2
          //if( init_trk.chi2_x > 2.*fChi2ndfMax ) continue; // 2 degrees of freedom
          //if( init_trk.chi2_y > 2.*fChi2ndfMax ) continue; // 2 degrees of freedom

          //maximal track reduced chi2 in the xy plane
          if( TrackChi2(x, y, init_trk) > 4.*fChi2ndfMax ) continue; // 4 degrees of freedom in the xy plane

          //the track is selected

          //evaluate clusters making the track
          TagMapsBasicPlane::Cluster *cls[] = {&c1, &c2, &c3, &c4};
          init_trk.cls.assign(cls, cls+4); // clusters in the track
          ClusterAnalysis(cls, init_trk);

          //add the track for the event
          fTracks.push_back( init_trk );
          Track& trk = fTracks.back();

          //track for primary particle
          trk.is_prim = c1.is_prim and c2.is_prim and c3.is_prim and c4.is_prim;

          //MC particle corresponding to the track, set for all clusters from the same MC particle
          if( (c1.itrk == c2.itrk) and (c2.itrk == c3.itrk) and (c3.itrk == c4.itrk) ) {

            trk.itrk = c1.itrk;
            trk.pdg = c1.pdg;
          }

          //primary particle ID, set to the track when the primary ID is the same for all clusters
          if( (c1.prim_id == c2.prim_id) and (c2.prim_id == c3.prim_id) and (c3.prim_id == c4.prim_id) ) {

            trk.prim_id = c1.prim_id;
          }

          //increment event quantities
          fNtrk++;
          if( trk.is_prim ) fNtrkPrim++;
          if( trk.itrk == 1 ) fAllTrkSig++;

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

  //cout << "Track: " << pos << " " << slope << " " << theta << " " << chi2 << endl;

}//MakeTrack

//_____________________________________________________________________________
Double_t TagMapsBasic::TrackChi2(Double_t *x, Double_t *y, Track& trk) {

  //calculate track chi^2 for its points
  Double_t chi2_xy = 0;

  //points loop
  for(int i=0; i<4; i++) {

    //track position in x and y
    Double_t track_x_i = trk.x + trk.slope_x*fZ[i];
    Double_t track_y_i = trk.y + trk.slope_y*fZ[i];

    //square distance between the track and measured point along x and y
    Double_t dx2 = (track_x_i-x[i])*(track_x_i-x[i]);
    Double_t dy2 = (track_y_i-y[i])*(track_y_i-y[i]);

    //add the square distance in the xy plane to the chi^2
    chi2_xy += dx2 + dy2;

    //cout << i << ": " << track_x_i-x[i] << " " << track_y_i-y[i] << " ";
    //cout << i << ": " << dx2 << " " << dy2 << " ";

  }//points loop

  //set the chi^2 for the track
  trk.chi2_xy = chi2_xy;

  return chi2_xy;

}//TrackChi2

//_____________________________________________________________________________
template<size_t N> void TagMapsBasic::ClusterAnalysis(TagMapsBasicPlane::Cluster* (&cls)[N], Track& trk) {

  //cout << "Clusters:";

  unordered_set<Int_t> itrk; // MC track indices from the clusters

  //cluster loop
  for(size_t icls=0; icls<N; icls++) {

    //increment track counts for the cluster
    cls[icls]->ntrk += 1;

    itrk.insert( cls[icls]->itrk ); // add the MC track index

    //cout << " " << cls[icls]->iplane << " " << cls[icls]->id;
    //cout << " " << cls[icls]->itrk;

  }//cluster loop

  trk.num_diff_itrk = itrk.size(); // number of unique MC track indices

  //cout << " " << itrk.size();
  //cout << endl;

}//ClusterAnalysis

//_____________________________________________________________________________
void TagMapsBasic::SetClsLimMdist(Double_t d) {

  //set limit on minimal cluster distance for all planes

  //plane loop
  for(auto i: fPlanes) {

    i->SetLimMdist(d);
  }//plane loop

}//SetClsLimMdist

//_____________________________________________________________________________
void TagMapsBasic::FinishEvent() {

  //G4cout << "TagMapsBasic::FinishEvent, " << fNam << G4endl;

  //finish for planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fn( &TagMapsBasicPlane::FinishEvent ));

  //set output tree for tracks

  //counter for associated tracks in event
  fNtrkAssociated = 0;

  //reconstruction flags
  fIsSigTrk = kFALSE;
  fIsSigRec = kFALSE;
  fSigRecQ2 = 0;

  //tracks loop
  for(auto it = fTracks.begin(); it != fTracks.end(); it++) {

    //cout << "Track:";

    Int_t nshared = 0; // num of shared clusters

    //clusters for the track
    for(auto c1: (*it).cls) {

      //inner tracks loop
      for(auto it2 = fTracks.begin(); it2 != fTracks.end(); it2++) {
        if( it == it2 ) continue; //same track
        //inner clusters
        for(auto c2: (*it2).cls) {
          if( (c1->iplane == c2->iplane) and (c1->id == c2->id) ) {
            nshared++;
          }
        }//inner clusters
      }//inner tracks loop

    }//clusters for the track

    (*it).num_shared_cls = nshared; // set the number of shared clusters for the track

    //load MC particle for the track

    //MC loop
    for(unsigned long imc=0; imc<fMCItrk->size(); imc++) {

      //primary particle for the track
      if( fMCItrk->at(imc) != (*it).prim_id ) continue;

      //set MC kinematics for the track
      (*it).mcp_en = fMCEn->at(imc);
      (*it).mcp_theta = fMCTheta->at(imc);
      (*it).mcp_phi = fMCPhi->at(imc);
      (*it).mcp_Q2 = 2*18*(*it).mcp_en*(1-TMath::Cos(TMath::Pi()-(*it).mcp_theta));

      //cout << "MC: " << fMCItrk->at(imc) << ", energy: " << fMCEn->at(imc) << " " << (*it).mcp_en << endl;

    }//MC loop

    //cout << " shared clusters: " << (*it).num_shared_cls << endl;

    //set the output track and fill the tree
    fOutTrk = *it; // load the current track
    fOutTrk.evt_ntrk = fNtrk; // set number of tracks in event for the track
    if( fOutTrk.is_associate ) fNtrkAssociated++; // counts for associated tracks

    fTrkTree->Fill();

    //reconstruction flags for signal track
    if( (*it).prim_id == 1 ) {
      fIsSigTrk = kTRUE; // signal track is present

      if( (*it).is_rec == kTRUE ) {
        fIsSigRec = kTRUE; // Q^2 is reconstructed for signal track
        fSigRecQ2 = (*it).rec_Q2; // value of the Q^2
      }
    }

  } //tracks loop

}//FinishEvent

//_____________________________________________________________________________
void TagMapsBasic::CreateOutput(bool planes) {

  //create output for individual planes
  if(planes) {
    for_each(fPlanes.begin(), fPlanes.end(), mem_fn( &TagMapsBasicPlane::CreateOutput ));
  }

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
  fTrkTree->Branch("chi2_xy", &fOutTrk.chi2_xy, "chi2_xy/D");
  fTrkTree->Branch("is_prim", &fOutTrk.is_prim, "is_prim/O");
  fTrkTree->Branch("itrk", &fOutTrk.itrk, "itrk/I");
  fTrkTree->Branch("prim_id", &fOutTrk.prim_id, "prim_id/I");
  fTrkTree->Branch("is_associate", &fOutTrk.is_associate, "is_associate/O");
  fTrkTree->Branch("ref_x", &fOutTrk.ref_x, "ref_x/D");
  fTrkTree->Branch("ref_y", &fOutTrk.ref_y, "ref_y/D");
  fTrkTree->Branch("ref_theta_x", &fOutTrk.ref_theta_x, "ref_theta_x/D");
  fTrkTree->Branch("ref_theta_y", &fOutTrk.ref_theta_y, "ref_theta_y/D");
  fTrkTree->Branch("evt_ntrk", &fOutTrk.evt_ntrk, "evt_ntrk/I");
  fTrkTree->Branch("num_shared_cls", &fOutTrk.num_shared_cls, "num_shared_cls/I");
  fTrkTree->Branch("num_diff_itrk", &fOutTrk.num_diff_itrk, "num_diff_itrk/I");
  fTrkTree->Branch("is_rec", &fOutTrk.is_rec, "is_rec/O");
  fTrkTree->Branch("rec_en", &fOutTrk.rec_en, "rec_en/D");
  fTrkTree->Branch("rec_theta", &fOutTrk.rec_theta, "rec_theta/D");
  fTrkTree->Branch("rec_phi", &fOutTrk.rec_phi, "rec_phi/D");
  fTrkTree->Branch("rec_Q2", &fOutTrk.rec_Q2, "rec_Q2/D");
  fTrkTree->Branch("mcp_en", &fOutTrk.mcp_en, "mcp_en/D");
  fTrkTree->Branch("mcp_theta", &fOutTrk.mcp_theta, "mcp_theta/D");
  fTrkTree->Branch("mcp_phi", &fOutTrk.mcp_phi, "mcp_phi/D");
  fTrkTree->Branch("mcp_Q2", &fOutTrk.mcp_Q2, "mcp_Q2/D");
  fTrkTree->Branch("ninp", &fOutTrk.ninp, "ninp/I");

  //event quantities
  fEvtTree->Branch((fNam+"_ntrk").c_str(), &fNtrk, (fNam+"_ntrk/I").c_str());
  fEvtTree->Branch((fNam+"_ntrk_prim").c_str(), &fNtrkPrim, (fNam+"_ntrk_prim/I").c_str());
  fEvtTree->Branch((fNam+"_ntrk_associate").c_str(), &fNtrkAssociated, (fNam+"_ntrk_associate/I").c_str());
  fEvtTree->Branch((fNam+"_is_sig_trk").c_str(), &fIsSigTrk, (fNam+"_is_sig_trk/O").c_str());
  fEvtTree->Branch((fNam+"_is_sig_rec").c_str(), &fIsSigRec, (fNam+"_is_sig_rec/O").c_str());
  fEvtTree->Branch((fNam+"_sig_rec_Q2").c_str(), &fSigRecQ2, (fNam+"_sig_rec_Q2/D").c_str());

}//CreateOutput

//_____________________________________________________________________________
void TagMapsBasic::AddTrackBranch(string nam, Double_t *val) {

  //add a branch to the station output tree

  fTrkTree->Branch(nam.c_str(), val, (nam+"/D").c_str());

}//AddTrackBranch

//_____________________________________________________________________________
void TagMapsBasic::WriteOutputs() {

  //write outputs for the planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fn( &TagMapsBasicPlane::WriteOutputs ));

  cout << "Tagger " << fNam << ", tracks: " << fTrkTree->GetEntries() << ", signal tracks: " << fAllTrkSig << endl;

  fTrkTree->Write();

}//WriteOutputs

//_____________________________________________________________________________
int TagMapsBasic::GetNumberOfClusters(int iplane) {

  //number of clusters at iplane

  return fPlanes[iplane]->GetClusters().size();

}//GetNumberOfClusters

//_____________________________________________________________________________
int TagMapsBasic::GetNumberOfClusters() {

  //number of clusters at all planes

  int ncls = 0;

  for(auto i: fPlanes) {

    ncls += i->GetClusters().size();
  }

  return ncls;

}//GetNumberOfClusters

//_____________________________________________________________________________
void TagMapsBasic::GetCluster(int iplane, int icls, double& x, double& y, double& z, double& md) {

  //cluster icls at iplane
  TagMapsBasicPlane::Cluster& cls = fPlanes[iplane]->GetClusters()[icls];

  //position
  x = cls.x;
  y = cls.y;
  z = fZ[iplane];

  //minimal distance to another cluster on the plane
  md = cls.min_dist;

}//GetCluster

//_____________________________________________________________________________
void TagMapsBasic::SetMCParticles(vector<Int_t> *itrk, vector<Double_t> *en, vector<Double_t> *theta, vector<Double_t> *phi) {

  //set branches with MC particles

  fMCItrk = itrk;
  fMCEn = en;
  fMCTheta = theta;
  fMCPhi = phi;

}//SetMCParticles


























