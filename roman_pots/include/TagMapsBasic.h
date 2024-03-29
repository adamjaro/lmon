
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

    void CreateOutput(bool planes=true);
    void AddTrackBranch(std::string nam, Double_t *val);
    void WriteOutputs();

    void SetMaxChi2Ndf(Double_t max_chi2ndf) { fChi2ndfMax = max_chi2ndf; }
    void SetClsLimMdist(Double_t d);

    void SetMCParticles(std::vector<Int_t>*, std::vector<Double_t>*, std::vector<Double_t>*, std::vector<Double_t>*);

    void FinishEvent();

    class Track;
    std::vector<Track>& GetTracks() { return fTracks; }

    int GetNumberOfClusters(int iplane);
    int GetNumberOfClusters();
    void GetCluster(int iplane, int icls, double& x, double& y, double& z, double& md);

    std::string GetName() { return fNam; }
    Double_t GetMaxChi2ndf() { return fChi2ndfMax; }
    Double_t GetClsLimMdist() { return fPlanes[0]->GetLimMdist(); }

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
        chi2_x(0), chi2_y(0), chi2_xy(0), is_prim(0), itrk(-1), pdg(0), prim_id(-1), is_associate(0),
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
      Int_t prim_id; // ID of primary particle associated with the track
      Bool_t is_associate; // track association to a reference MC particle
      Double_t ref_x; // reference position in x, mm
      Double_t ref_y; // reference position in y, mm
      Double_t ref_theta_x; // reference angle along x, rad
      Double_t ref_theta_y; // reference angle along y, rad
      Int_t evt_ntrk; // number of all tracks in event for a given track
      Int_t num_shared_cls; // number of track clusters shared with another track
      Int_t num_diff_itrk; // number of unique MC track indices in the clusters
      Bool_t is_rec = 0; // reconstruction flag, 1 = track is reconstructed
      Double_t rec_en = 0; // reconstructed electron energy, GeV
      Double_t rec_theta = 0; // electron polar angle, rad
      Double_t rec_phi = 0; // electron azimuthal angle, rad
      Double_t rec_Q2 = 0; // reconstructed electron Q^2, GeV^2
      Double_t mcp_en = 0; // MC particle energy, GeV
      Double_t mcp_theta = 0; // MC particle polar angle, rad
      Double_t mcp_phi = 0; // MC particle azimuthal angle, rad
      Double_t mcp_Q2 = 0; // MC particle Q^2, GeV^2
      Int_t ninp = 0; //number of inputs used for reconstruction

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
    Bool_t fIsSigTrk; // flag for signal track presence (itrk == 1)
    Bool_t fIsSigRec; // flag for Q^2 reconstruction for signal track
    Double_t fSigRecQ2; // Q^2 for signal track

    //all track counter
    Int_t fAllTrkSig; // number of all signal tracks (itrk == 1)

    //MC particles
    std::vector<Int_t> *fMCItrk; // track ID for the particle
    std::vector<Double_t> *fMCEn; // particle energy, GeV
    std::vector<Double_t> *fMCTheta; // particle polar angle, rad
    std::vector<Double_t> *fMCPhi; // particle azimuthal angle, rad

};

#endif












