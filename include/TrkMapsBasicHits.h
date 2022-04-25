
#ifndef TrkMapsBasicHits_h
#define TrkMapsBasicHits_h

// Hits for TrkMapsBasic

class TrkMapsBasicHits {

  public:

    TrkMapsBasicHits() {}

    void AddSignal(G4Step *step);
    void CreateOutput(G4String nam, TTree *tree);
    void ClearEvent();
    void FinishEvent();

    void ConnectInput(std::string nam, TTree *tree);
    void LoadHits();
    unsigned long GetNhits() { return fHitsR.size(); }

    //hit representation
    class Hit {
    public:

      Hit(Int_t ip, Int_t ir, Double_t xp, Double_t yp, Double_t zp, Int_t it, Int_t pd):
        ipix(ip), irow(ir), x(xp), y(yp), z(zp), en(0), itrk(it), pdg(pd) {}

      Int_t ipix; // pixel index in the row
      Int_t irow; // row index in the layer
      Double_t x; // hit position in x, mm
      Double_t y; // hit position in y, mm
      Double_t z; // hit position in z, mm
      Double_t en; // hit energy, keV
      Int_t itrk; // track index
      Int_t pdg; // track PDG code

    };//Hit

  private:

    //run-time containers for hits
    std::map<std::pair<Int_t, Int_t>, Hit> fHitsW; // structure for write
    std::vector<Hit> fHitsR; // structure for read

    //output representation for hits
    std::vector<Int_t> *fIpix; // pixel index in the row
    std::vector<Int_t> *fIrow; // row index in the layer

    std::vector<Double_t> *fX; // hit position in x, mm
    std::vector<Double_t> *fY; // hit position in y, mm
    std::vector<Double_t> *fZ; // hit position in z, mm
    std::vector<Double_t> *fEn; // hit energy, keV

    std::vector<Int_t> *fItrk; // track index
    std::vector<Int_t> *fPdg; // track PDG code

};

#endif













