
#ifndef rcalc_h
#define rcalc_h

class TTree;
class TFile;

#include "Rtypes.h"

class rcalc {

  public:

    rcalc();
    ~rcalc();

    void open_input(std::string infile);
    void create_output(std::string outfile);
    void event_loop(int n=-1);

  private:

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

    //output tree
    TFile *outp;
    TTree *otree;

    Double_t zpos;
    Double_t rpos;
    Double_t en;

};

#endif

