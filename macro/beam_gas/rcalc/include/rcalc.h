
#ifndef rcalc_h
#define rcalc_h

class TTree;
class TFile;

#include "Rtypes.h"

class rcalc {

  public:

    rcalc(std::string nam);
    ~rcalc();

    void set_rmin(double r) { rmin = r; }

    void open_input(std::string infile);
    void create_output(std::string outfile);
    void event_loop(int n=-1);

  private:

    //detector name
    std::string det_name;

    Double_t rmin; // minimal selected radius, mm

    //input tree
    TFile *inp;
    TTree *tree;

    Double_t vtx_z; // z-vertex position, mm

    //hits array
    std::vector<Int_t> *hit_pdg; // particle pdg
    std::vector<Float_t> *hit_en; // hit energy, GeV
    std::vector<Float_t> *hit_x; // hit position in x, mm
    std::vector<Float_t> *hit_y; // hit position in y, mm
    std::vector<Float_t> *hit_z; // hit position in z, mm

    //output trees
    TFile *outp;
    TTree *ptree;
    TTree *etree;

    Double_t phot_zpos;
    Double_t phot_rpos;
    Double_t phot_en;

    Double_t el_zpos;
    Double_t el_rpos;
    Double_t el_en;

};

#endif

