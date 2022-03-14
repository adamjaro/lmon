
#ifndef TagCounter_h
#define TagCounter_h

// Tagger station with counting planes

class GeoParser;
class TagCounterPlane;

//_____________________________________________________________________________
class TagCounter {

  public:

    TagCounter(std::string nam, TTree *tree , TTree *otree, GeoParser *geo);

    void ProcessEvent();

    void CreateOutput(bool create_planes=false);
    void AddOutputBranch(std::string nam, Double_t *val);
    void WriteOutputs();

    Bool_t GetIsHit() { return fIsHit; }
    Double_t GetX() { return fX; }
    Double_t GetY() { return fY; }
    Double_t GetZ() { return fZ; }
    Double_t GetThetaX() { return fThetaX; }
    Double_t GetThetaY() { return fThetaY; }

  private:

    Double_t GetTheta(Double_t xy0, Double_t z0, Double_t xy1, Double_t z1);

    std::string fNam; // station name
    std::vector<TagCounterPlane*> fPlanes; // planes for the station

    Bool_t fIsHit; // flag for hit in station
    Int_t fNPlane; // number of planes with hit in event
    Int_t fNA; // number of hits in plane A in event
    Int_t fNB; // number of hits in plane B in event
    Int_t fNC; // number of hits in plane C in event

    TTree *fSTree; // output tree for a given tagger station
    Double_t fX; // track position in x, mm
    Double_t fY; // track position in y, mm
    Double_t fZ; // track position in z, mm
    Double_t fThetaX; // track angle in x, rad
    Double_t fThetaY; // track angle in y, rad

};

#endif

