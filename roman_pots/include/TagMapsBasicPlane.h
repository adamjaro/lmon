
#ifndef TagMapsBasicPlane_h
#define TagMapsBasicPlane_h

// MAPS plane for tagger station

#include <list>

#include "TrkMapsBasicHits.h"

class TagMapsBasicPlane {

  public:

    TagMapsBasicPlane(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree);

    void ProcessEvent();
    void FinishEvent();

    void CreateOutput();
    void WriteOutputs();

    void SetLimMdist(Double_t d) { fClsMinLimMdist = d; }
    Double_t GetLimMdist() { return fClsMinLimMdist; }

    TrkMapsBasicHits& GetHits() { return fHits; }

    class Cluster;
    std::vector<Cluster>& GetClusters() { return fCls; }

  private:

    void LoadHits();
    unsigned long FindHitEmax();
    int FindAdjHits(unsigned long ih, std::list<unsigned long>& adj_hits);
    int GetHitsCount();
    void GradientTest(Cluster& cls);
    Int_t SignI(Int_t i) {return (0<i)-(i<0);}

    void PrintCluster(Cluster& cls);

    std::string fNam; // plane name
    TrkMapsBasicHits fHits; // hits for the plane

    std::map<unsigned long, bool> fHitStat; // status flags for hits in plane

    //selection criteria for hits
    Double_t fEmin; // keV, threshold in energy

    TTree *fTree; // plane output tree
    Double_t fX; // x of hit, mm
    Double_t fY; // y of hit, mm
    Double_t fZ; // z of hit, mm
    Double_t fE; // hit energy, keV
    Int_t fPdg; // pdg for the hit
    Int_t fId; // track id for the hit

    TTree *fEvtTree; // event output tree, provided from outside

    Int_t fNhit; // number of hits in plane in event
    Int_t fNhitPrim; // number of primary hits in plane in event
    Int_t fNCls; // number of clusters in event
    Int_t fNClsPrim; // number of primary clusters in event

    //cluster representation
  public:
    class Cluster {
    public:
      Cluster(): x(0), y(0), en(0), nhits(0), is_prim(1),
                 sigma_x(0), sigma_y(0), itrk(-1), pdg(0), prim_id(0),
                 ntrk(0), min_dist(-1), id(0), iplane(0), stat(kTRUE) {}

      Double_t x; // cluster x position, mm
      Double_t y; // cluster y position, mm
      Double_t en; // cluster energy, keV
      Int_t nhits; // number of hits for the cluster
      Bool_t is_prim; // flag for primary particle
      Double_t sigma_x; // uncertainty in cluster x position, mm
      Double_t sigma_y; // uncertainty in cluster y position, mm
      Int_t itrk; // MC track index associated with the cluster
      Int_t pdg; // PDG code for the MC track
      Int_t prim_id; // ID of primary particle associated with the cluster
      Int_t ntrk; // number of tracks for which the cluster was used
      Double_t min_dist; // minimal distance to another cluster, mm
      Int_t id; // cluster ID on the plane
      Int_t iplane; // plane ID
      Bool_t stat; // cluster status

      std::list<unsigned long> hits; // indices for hits contributing to cluster

      Double_t GetSigma(Double_t swx2, Double_t pos);

    };//Cluster
  private:

    Double_t fClsMinLimMdist; // limit on minimal distance to another cluster, mm

    std::vector<Cluster> fCls; // clusters in event

    //custers output tree
    TTree *fClsTree = 0; // clusters output tree
    Double_t fClsX; // x of cluster, mm
    Double_t fClsY; // y of cluster, mm
    Double_t fClsE; // cluster energy, keV
    Int_t fClsNhits; // number of hits in cluster
    Bool_t fClsPrim; // primary flag for cluster
    Double_t fClsSigX; // uncertainty in x of cluster, mm
    Double_t fClsSigY; // uncertainty in y of cluster, mm
    Int_t fClsNtrk; // number of tracks for which the cluster was used
    Double_t fClsMinDist; // minimal distance to another cluster, mm
};

#endif















