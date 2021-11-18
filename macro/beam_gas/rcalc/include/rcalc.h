
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

    //generated particles
    std::vector<Int_t> *gen_pdg; // generated pdg
    std::vector<Float_t> *gen_en; // generated energy, GeV

    //output hit tree
    TFile *outp;
    TTree *htree; // hit tree
    TTree *etree; // event tree

    Double_t zpos;
    Double_t rpos;
    Double_t en;
    Int_t pdg;

    Int_t nhits;
    Double_t phot_en;

};

#endif

