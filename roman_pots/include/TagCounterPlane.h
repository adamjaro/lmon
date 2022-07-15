
#ifndef TagCounterPlane_h
#define TagCounterPlane_h

// Counting plane for tagger station

class GeoParser;

#include "ParticleCounterHits.h"

class TagCounterPlane {

  public:

    TagCounterPlane(std::string nam, TTree *tree, GeoParser *geo);

    bool IsHit();
    Double_t GetX() { return fX; }
    Double_t GetY() { return fY; }
    Double_t GetZ() { return fZ; }
    Int_t GetNhit() { return nhit; }

    ParticleCounterHits& GetHits() { return fHits; }

    void CreateOutput();
    void WriteOutputs();

  private:

    std::string fNam; // plane name
    ParticleCounterHits fHits; // hits for the plane

    Int_t nhit; // number of hits in plane in event

    TTree *ptree; // plane output tree
    Double_t fX; // x of primary hit, mm
    Double_t fY; // y of primary hit, mm
    Double_t fZ; // z of primary hit, mm

    TTree *pair_tree; // pairs of hits
    Double_t fDx; // pair abs difference in x
    Double_t fDy; // pair abs difference in y
    Double_t fDxy; // pair abs difference in xy

};












#endif

