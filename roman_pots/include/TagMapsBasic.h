
#ifndef TagMapsBasic_h
#define TagMapsBasic_h

// Tagger station composed of MAPS basic planes

class TagMapsBasicPlane;
class GeoParser;
#include "TrkMapsBasicHits.h"

class TagMapsBasic {

  public:

    TagMapsBasic(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree);

    void ProcessEvent();

    void CreateOutput();
    void WriteOutputs();

  private:

    bool SelectHit(const TrkMapsBasicHits::Hit& hit);
    //void MakeTrack(Double_t x1, Double_t x2, Double_t x3, Double_t x4, );
    void MakeTrack(Double_t *x, Double_t& pos, Double_t& slope, Double_t& theta, Double_t& chi2);

    std::string fNam; // station name
    std::vector<TagMapsBasicPlane*> fPlanes; // planes for the station

    Double_t fEmin; // keV, threshold in energy

    Double_t fL; // plane spacing, mm
    Double_t fZ[4]; // local z positions for planes, mm

    //tracks tree
    TTree *fTrkTree;
    Double_t fPosX; // track position in x, mm
    Double_t fPosY; // track position in y, mm
    Double_t fSlopeX; // track slope in x
    Double_t fSlopeY; // track slope in y
    Double_t fThetaX; // track angle along x, rad
    Double_t fThetaY; // track angle along y, rad
    Double_t fChi2X; // track chi^2 in x
    Double_t fChi2Y; // track chi^2 in y
    Bool_t fPrim; // track for primary particle

    //event quantities
    TTree *fEvtTree;
    Int_t fNtrk; // number of tracks per event
    Int_t fNtrkPrim; // number of primary tracks per event

};

#endif












