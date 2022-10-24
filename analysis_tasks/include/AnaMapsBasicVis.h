
#ifndef AnaMapsBasicVis_h
#define AnaMapsBasicVis_h

#include "AnaMapsBasic.h"

class AnaMapsBasicVis : protected AnaMapsBasic {

  public:

    AnaMapsBasicVis(const char *conf);

    std::string GetDetName() { return tag->GetName(); }
    void SetDet(int i);

    int ProcessEvent(bool *stat=0x0);
    int NextEvent(int di=1);
    int PreviousEvent();
    void SetEvent(int i) { iev = i; }

    void SetMaxChi2ndf(double chi2);

    void SetMinNtrk(int n) { min_ntrk = n; }

    int GetNumberOfClusters(int iplane);
    void GetCluster(int iplane, int icls, double& x, double& y, double& z, double& md);

    int GetNumberOfTracks();
    void GetTrack(int i, double& x0, double& y0, double& slope_x, double& slope_y, double& chi2);

    int GetNumberOfRefTracks();

    Double_t GetMaxChi2ndf() { return tag->GetMaxChi2ndf(); }

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
    RefCounter *cnt; // active reference counter

    unsigned long min_ntrk; // minimal number of tracks in event

};



#endif

