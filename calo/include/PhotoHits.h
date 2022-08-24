
#ifndef PhotoHits_h
#define PhotoHits_h

// hits for optical detector

class PhotoHits {

  public:

    PhotoHits();

    void CreateOutput(G4String nam, TTree *tree);
    void ClearEvent();
    void FinishEvent();

    void ConnectInput(std::string nam, TTree *tree);
    void LoadHits();
    unsigned long GetNhits() { return fHits.size(); }

    //hit representation
    class Hit {
    public:

      Double_t pos_x; // hit position in x, mm
      Double_t pos_y; // hit position in y, mm
      Double_t pos_z; // hit position in z, mm
      Double_t time; // time of the hit, ns

    };//Hit

    //make new hit and return reference to it
    Hit& CreateHit() { fHits.push_back(Hit()); return fHits.back(); }
    Hit GetHit(unsigned long i) { return fHits[i]; }

  private:

    std::vector<Hit> fHits; // hit collection

    Hit fHitIO; // hit member of input/output

    //hit memory representation
    class HitParBase {
    public:
      virtual void CreateOutput(std::string tnam, TTree* tree) = 0;
      virtual void ClearEvent() = 0;
      virtual void Write() = 0;
      virtual void ConnectInput(std::string tnam, TTree* tree) = 0;
      virtual unsigned long GetN() = 0;
      virtual void LoadVal(unsigned long i) = 0;
    };
    template<typename T> class HitPar: public HitParBase {
      public:
        HitPar(std::string n, T& v): par_nam(n), val(v) {}
        void CreateOutput(std::string tnam, TTree* tree) {
          //create the vector and tree branch from provided detector name and parameter name
          vec = new std::vector<T>();
          tree->Branch((tnam+par_nam).c_str(), vec);
        }
        void ClearEvent() { vec->clear(); } //clear the vector for next event
        void Write() { vec->push_back(val); } // write the given value to the vector
        void ConnectInput(std::string tnam, TTree* tree) {
          //connect the vector to the input tree
          vec = 0x0;
          tree->SetBranchAddress((tnam+par_nam).c_str(), &vec);
        }
        unsigned long GetN() { return vec->size(); } // number of values for a given event
        void LoadVal(unsigned long i) { val = vec->at(i); } // load the value at the given position
      private:
        std::string par_nam; // parameter name
        T& val; // input/output value
        std::vector<T> *vec; // parameter values
    };//HitPar
    std::vector<HitParBase*> fHitPars; // hit parametes in its memory representation

};

#endif














