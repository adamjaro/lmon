
#ifndef TagMapsBasicPlane_h
#define TagMapsBasicPlane_h

// MAPS plane for tagger station

#include "TrkMapsBasicHits.h"

class TagMapsBasicPlane {

  public:

    TagMapsBasicPlane(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree);

    void LoadHits();

    void ProcessEvent();

    void CreateOutput();
    void WriteOutputs();

    TrkMapsBasicHits& GetHits() { return fHits; }

  private:

    std::string fNam; // plane name
    TrkMapsBasicHits fHits; // hits for the plane

    // for hits
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

};

#endif















