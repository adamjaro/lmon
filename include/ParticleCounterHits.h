
#ifndef ParticleCounterHits_h
#define ParticleCounterHits_h

// hits for ParticleCounter

class GeoParser;

class ParticleCounterHits {

  public:

    ParticleCounterHits();

    void AddHit();
    void CreateOutput(G4String nam, TTree *tree);
    void ClearEvent();

    //hit representation
    class CounterHit {
    public:

      CounterHit(): pdg(0), en(0), x(0), y(0), z(0), parentID(0) {}
      CounterHit(const CounterHit& h): pdg(h.pdg), en(h.en), x(h.x),
        y(h.y), z(h.z), parentID(h.parentID), itrk(h.itrk), is_prim(h.is_prim) {}
      CounterHit& operator=(const CounterHit& h) {
        pdg = h.pdg;
        en = h.en;
        x = h.x;
        y = h.y;
        z = h.z;
        parentID = h.parentID;
        itrk = h.itrk;
        is_prim = h.is_prim;
        return *this;
      }

      Int_t pdg; // particle pdg
      Float_t en; // hit energy, GeV
      Float_t x; // hit position in x, mm
      Float_t y; // hit position in y, mm
      Float_t z; // hit position in z, mm
      Int_t parentID; // parent ID for track in hit
      Int_t itrk; // track index
      Bool_t is_prim; // hit by primary particle

    };

    CounterHit& Hit() { return fHit; }

    void ConnectInput(std::string nam, TTree *tree);
    int GetNHits() { return fHitPdg->size(); }
    CounterHit GetHit(int i);

    void LocalFromGeo(G4String nam, GeoParser *geo);
    G4double GetXPos() { return fXpos; }
    void SetXPos(G4double x) { fXpos = x; }

    CounterHit GlobalToLocal(CounterHit in);

  private:

    //hit instance
    CounterHit fHit;

    //hits array
    std::vector<Int_t> *fHitPdg;
    std::vector<Float_t> *fHitEn;
    std::vector<Float_t> *fHitX;
    std::vector<Float_t> *fHitY;
    std::vector<Float_t> *fHitZ;
    std::vector<Int_t> *fHitParentID;
    std::vector<Int_t> *fHitItrk; // track index
    std::vector<Bool_t> *fHitPrim; // primary flag

    G4double fXpos; // counter position in x, mm
    G4double fYpos; // counter position in y, mm
    G4double fZpos; // counter position in z, mm
    G4double fTheta_x; // counter rotation along x, rad
    G4double fTheta_y; // counter rotation along y, rad

};

#endif

