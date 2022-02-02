
#ifndef CaloBPCHits_h
#define CaloBPCHits_h

// Hits for CaloBPC

class CaloBPCHits {

  public:

    CaloBPCHits() {}

    void SetScinPos(G4int istrip, G4double pos);
    void AddSignal(G4int istrip, G4int ilay, G4double en);

    void CreateOutput(G4String nam, TTree *tree);
    void ClearEvent();
    void FinishEvent();

    void ConnectInput(std::string nam, TTree *tree);
    void LoadHits();
    unsigned long GetNhits() { return fHits.size(); }

    //hit representation
    class Hit {
    public:

      Hit(Int_t isc, Bool_t ver, Double_t xp, Double_t yp): iscin(isc), vert(ver),
        en(0), x(xp), y(yp), z(0) {}

      Int_t iscin; // scintillator index
      Bool_t vert; // vertical (true) or horizontal (false)
      Double_t en; // hit energy, GeV
      Double_t x; // hit position in x, mm
      Double_t y; // hit position in y, mm
      Double_t z; // hit position in z, mm

    };

    const Hit& GetHit(unsigned long i) { return fHits[i]; }

  private:

    void WriteHits(std::map<Int_t, Hit> *hits);

    std::map<G4int, G4double> fXYpos; // scintillator positions, mm

    //run-time containers for hits
    std::map<Int_t, Hit> fVerHits, fHorHits; // vertical and horizontal hits
    std::vector<Hit> fHits;

    //output representation for hits
    std::vector<Int_t> *fIscin; // scintillator index
    std::vector<Bool_t> *fVert; // vertical (true) or horizontal (false)
    std::vector<Double_t> *fEn; // hit energy, GeV
    std::vector<Double_t> *fX; // hit position in x, mm
    std::vector<Double_t> *fY; // hit position in y, mm
    std::vector<Double_t> *fZ; // hit position in z, mm

};

#endif

