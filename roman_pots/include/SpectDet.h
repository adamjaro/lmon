
#ifndef SpectDet_h
#define SpectDet_h

// Spectrometer detecting station

#include "CaloBPCHits.h"
class SpectPlane;

class SpectDet {

  public:

    SpectDet(std::string nam, std::string geo_nam, TTree *tree, GeoParser *geo);

    void SetLayEmin(double emin);
    void SetLayPdg(int pdg);
    void SetCalEmin(Double_t emin) { fCalEmin = emin; }

    bool IsHit();

    Double_t GetX() { return fX; }
    Double_t GetY() { return fY; }
    Double_t GetZ() { return fZ; }
    Double_t GetThetaX() { return fThetaX; }
    Double_t GetThetaY() { return fThetaY; }
    Double_t GetCalE() { return fCalE; }

    void CreateOutput();
    void WriteOutputs();

  private:

    Double_t GetTheta(Double_t xyA, Double_t zA, Double_t xyC, Double_t zC);

    std::string fNam; // detector name

    Double_t fCalEmin; // minimal calorimeter energy, GeV

    std::vector<SpectPlane*> fLay; // tracking layers

    CaloBPCHits fCal; // calorimeter hits

    TTree *fSTree; // output tree for a given spectrometer
    Double_t fX; // track position in x, mm
    Double_t fY; // track position in y, mm
    Double_t fZ; // track position in z, mm
    Double_t fThetaX; // track angle in x, mrad
    Double_t fThetaY; // track angle in y, mrad
    Double_t fCalE; // calorimeter deposited energy, GeV

};

#endif

