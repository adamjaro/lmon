
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

    void CreateOutput();
    void WriteOutputs();

  private:

    std::string fNam; // plane name
    ParticleCounterHits fHits; // hits for the plane

    TTree *ptree; // plane output tree
    Double_t fX; // x of primary hit, mm
    Double_t fY; // y of primary hit, mm
    Double_t fZ; // z of primary hit, mm

};












#endif

