
#ifndef TagMapsBasicPlane_h
#define TagMapsBasicPlane_h

// MAPS plane for tagger station

#include "TrkMapsBasicHits.h"

class TagMapsBasicPlane {

  public:

    TagMapsBasicPlane(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree);

    void ProcessEvent();

    void CreateOutput();
    void WriteOutputs();

    TrkMapsBasicHits& GetHits() { return fHits; }

  private:

    void LoadHits();
    unsigned long FindHitEmax();
    int FindAdjHits(unsigned long ih, std::vector<unsigned long>& adj_hits);
    int GetHitsCount();

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
    class Cluster {
    public:
      Cluster(): x(0), y(0), en(0), nhits(0), is_prim(1) {}

      Double_t x; // cluster x position, mm
      Double_t y; // cluster y position, mm
      Double_t en; // cluster energy, keV
      Int_t nhits; // number of hits for the cluster
      Bool_t is_prim; // flag for primary particle

      std::vector<unsigned long> hits; // indices for hits contributing to cluster

    };//Cluster

    std::vector<Cluster> fCls; // clusters in event

    //custers output tree
    TTree *fClsTree; // clusters output tree
    Double_t fClsX; // x of cluster, mm
    Double_t fClsY; // y of cluster, mm
    Double_t fClsE; // cluster energy, keV
    Int_t fClsNhits; // number of hits in cluster
    Bool_t fClsPrim; // primary flag for cluster

};

#endif















