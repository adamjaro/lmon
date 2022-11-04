
#ifndef RefCounter_h
#define RefCounter_h

// Reference counter consisting of two planes placed along z

class TagCounterPlane;
class TH1D;

//_____________________________________________________________________________
class RefCounter {

  public:

    RefCounter(std::string nam, TTree *tree, GeoParser *geo, TTree *otree);

    void ProcessEvent();
    void FinishEvent();
    void WriteOutputs();

    class Track;
    std::vector<Track>& GetTracks() { return fTracks; }

  private:

    std::string fNam; // station name

    TagCounterPlane *fP1; // plane 1, lower z
    TagCounterPlane *fP2; // plane 2 at larger z

    Int_t fNtrk; // number of tracks in event
    Int_t fNtrkPrim; // number of primary tracks in event
    Bool_t fHitPrim; // flag for hit by primary particle in event

    TTree *fTrackTree; // track output tree
    Double_t fX; // track position in x, mm
    Double_t fY; // track position in y, mm
    Double_t fThetaX; // track angle in x, rad
    Double_t fThetaY; // track angle in y, rad
    Bool_t fPrim; // track for primary particle
    Bool_t fRec; // the track was reconstructed when true

    enum fTrkCount {kAll=1, kRec, kMaxCnt};
    TH1D *fCnt; // track counter

    //track in reference counter
  public:
    class Track {
    public:
      Track(): x(0), y(0), theta_x(0), theta_y(0),
               is_prim(0), itrk(-1), pdg(0), is_rec(0) {}

      Double_t x; // track position in x, mm
      Double_t y; // track position in y, mm
      Double_t theta_x; // track angle along x, rad
      Double_t theta_y; // track angle along y, rad
      Bool_t is_prim; // track for primary particle
      Int_t itrk; // index for MC particle
      Int_t pdg; // pdg for MC particle
      Bool_t is_rec; // the track was reconstructed when true

    };//Track

  private:

    std::vector<Track> fTracks; // reference tracks in event

};

#endif

