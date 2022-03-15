
#ifndef SpectDet_h
#define SpectDet_h

// Spectrometer detecting station

class SpectPlane;

class SpectDet {

  public:

    SpectDet(std::string nam, std::string geo_nam, TTree *tree, GeoParser *geo);

    void SetLayEmin(double emin);
    void SetLayPdg(int pdg);

    void ProcessEvent();

    void CreateOutput();
    void WriteOutputs();

  private:

    std::vector<SpectPlane*> fLay; // tracking layers

};

#endif

