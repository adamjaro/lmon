
#ifndef TagMapsBasic_h
#define TagMapsBasic_h

// Tagger station composed of MAPS basic planes

class GeoParser;
#include "TrkMapsBasicHits.h"
#include "TagMapsBasicPlane.h"

class TagMapsBasic {

  public:

    TagMapsBasic(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree);

    void ProcessEvent();

    void CreateOutput();
    void AddTrackBranch(std::string nam, Double_t *val);
    void WriteOutputs();

    void SetMaxChi2Ndf(Double_t max_chi2ndf) { fChi2ndfMax = max_chi2ndf; }

    void FinishEvent();

    class Track;
    std::vector<Track>& GetTracks() { return fTracks; }

  private:

    void MakeTrack(Double_t *x, Double_t& pos, Double_t& slope, Double_t& theta, Double_t& chi2);

    std::string fNam; // station name
    std::vector<TagMapsBasicPlane*> fPlanes; // planes for the station

    Double_t fChi2ndfMax; // maximal reduced chi2 for tracks

    Double_t fL; // plane spacing, mm
    Double_t fZ[4]; // local z positions for planes, mm

    //track representation
  public:
    class Track {
    public:
      Track(): x(0), y(0), slope_x(0), slope_y(0), theta_x(0), theta_y(0),
        chi2_x(0), chi2_y(0), chi2_xy(0), is_prim(0), itrk(-1), pdg(0), is_associate(0),
        ref_x(0), ref_y(0), ref_theta_x(0), ref_theta_y(0), evt_ntrk(0), num_shared_cls(0),
        num_diff_itrk(0), cls(0) {}

      Double_t x; // track position in x, mm
      Double_t y; // track position in y, mm
      Double_t slope_x; // track slope in x
      Double_t slope_y; // track slope in y
      Double_t theta_x; // track angle along x, rad
      Double_t theta_y; // track angle along y, rad
      Double_t chi2_x; // track chi^2 in x
      Double_t chi2_y; // track chi^2 in y
      Double_t chi2_xy; // track chi^2 in xy plane
      Bool_t is_prim; // track for primary particle
      Int_t itrk; // index for MC particle
      Int_t pdg; // pdg for MC particle
      Bool_t is_associate; // track association to a reference MC particle
      Double_t ref_x; // reference position in x, mm
      Double_t ref_y; // reference position in y, mm
      Double_t ref_theta_x; // reference angle along x, rad
      Double_t ref_theta_y; // reference angle along y, rad
      Int_t evt_ntrk; // number of all tracks in event for a given track
      Int_t num_shared_cls; // number of track clusters shared with another track
      Int_t num_diff_itrk; // number of unique MC track indices in the clusters

      std::vector<TagMapsBasicPlane::Cluster*> cls; // track clusters

    };//Track

  private:

    Double_t TrackChi2(Double_t *x, Double_t *y, Track& trk);

    template<std::size_t N>
    void ClusterAnalysis(TagMapsBasicPlane::Cluster* (&cls)[N], Track& trk);

    std::vector<Track> fTracks; // tracks in event

    //tracks tree
    TTree *fTrkTree;
    Track fOutTrk; // track instance for output tree

    //event quantities
    TTree *fEvtTree;
    Int_t fNtrk; // number of tracks per event
    Int_t fNtrkPrim; // number of primary tracks per event
    Int_t fNtrkAssociated; // number of tracks associated with MC particle

};

#endif












