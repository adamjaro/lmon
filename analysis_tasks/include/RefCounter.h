
#ifndef RefCounter_h
#define RefCounter_h

// Reference counter consisting of two planes placed along z

class TagCounterPlane;

//_____________________________________________________________________________
class RefCounter {

  public:

    RefCounter(std::string nam, TTree *tree, GeoParser *geo, TTree *otree);

    void ProcessEvent();

    void WriteOutputs();

  private:

    std::string fNam; // station name

    TagCounterPlane *fP1; // plane 1, lower z
    TagCounterPlane *fP2; // plane 2 at larger z

    Int_t fNtrk; // number of tracks in event
    Int_t fNtrkPrim; // number of primary tracks in event

    TTree *fTrackTree; // track output tree
    Double_t fX; // track position in x, mm
    Double_t fY; // track position in y, mm
    Double_t fThetaX; // track angle in x, rad
    Double_t fThetaY; // track angle in y, rad
    Bool_t fPrim; // track for primary particle

};

#endif

