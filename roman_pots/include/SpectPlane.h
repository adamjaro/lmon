
#ifndef SpectPlane_h
#define SpectPlane_h

// Counting plane for luminosity spectrometer

class GeoParser;

#include "ParticleCounterHits.h"

class SpectPlane {

  public:

    SpectPlane(std::string nam, std::string geo_nam, TTree *tree, GeoParser *geo);

    void SetEmin(double emin) { fEmin = emin; }
    void SetPdgSel(int pdg) { fPdgSel = pdg; }

    bool IsHit();

    Double_t GetX() { return fX; }
    Double_t GetY() { return fY; }
    Double_t GetZ() { return fZ; }

    void CreateOutput();
    void WriteOutputs();

  private:

    std::string fNam; // plane name
    ParticleCounterHits fHits; // hits for the plane

    double fEmin; // GeV, minimal energy
    int fPdgSel; // pdg selection

    TTree *ltree; // layer output tree
    Double_t fX; // x of hit, mm
    Double_t fY; // y of hit, mm
    Double_t fZ; // z of hit, mm
    Double_t fEn; // hit energy, GeV
    Int_t fPdg; // hit pdg

};

#endif

