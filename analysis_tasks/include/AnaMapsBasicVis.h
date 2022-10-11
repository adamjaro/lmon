
#ifndef AnaMapsBasicVis_h
#define AnaMapsBasicVis_h

#include "AnaMapsBasic.h"

class AnaMapsBasicVis : protected AnaMapsBasic {

  public:

    AnaMapsBasicVis(const char *conf);

    void NextEvent();

    int GetNumberOfClusters(int iplane);
    void GetCluster(int iplane, int icls, double& x, double& y, double& z);

    int GetNumberOfTracks();
    void GetTrack(int i, double& x0, double& y0, double& slope_x, double& slope_y);

  private:

    TChain *tree; // input tree
    TFile *out; // output file
    TTree *otree; // output tree

    TagMapsBasic *s1; // Tagger 1
    TagMapsBasic *s2; // Tagger 2

    RefCounter *cnt_s1; // Reference counter 1
    RefCounter *cnt_s2; // Reference counter 2

    Long64_t iev; // event number

    TagMapsBasic *tag; // active tagger

};



#endif

