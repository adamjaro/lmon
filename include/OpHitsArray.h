
#ifndef OpHitsArray_h
#define OpHitsArray_h

//hits array for optical photon detector

class OpHitsArray {

  public:

    OpHitsArray(G4double dt);

    void CreateOutput(std::string nam, TTree *tree);

    void Clear();

    void AddHit(G4double time);

    void WriteOutput();

  private:

    G4double fDt; // ns, time interval for a single hit

    //hit description
    struct hit {

      //hit() {} // for alternative approach with iterator
      //hit(Double_t tim): fTime(tim), fNphot(0) {G4cout << "hit" << G4endl;}
      hit(): fTime(0), fNphot(0) {}

      Float_t fTime; // time of the hit
      Int_t fNphot; // number of photoelectrons in hit
    };

    std::map<int, hit> fHits; // map holding the hits

    std::vector<Float_t> fHitsTime; // output hits time
    std::vector<Int_t> fHitsNphot; // output number of photoelectrons in hits

};

#endif














