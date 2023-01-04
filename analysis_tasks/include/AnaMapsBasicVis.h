
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
    void SetClsLimMdist(double d);

    void SetMinNtrk(int n) { min_ntrk = n; }
    void SetMinNcls(int n) { min_ncls = n; }
    void SetMinNcnt(int n) { min_ncnt = n; }
    void SetMinEtrk(int n) { min_etrk = n; }

    int GetNumberOfClusters(int iplane);
    void GetCluster(int iplane, int icls, double& x, double& y, double& z, double& md);

    int GetNumberOfTracks();
    int GetSigTracks();
    void GetTrack(int i, double& x0, double& y0, double& slope_x, double& slope_y, double& chi2, int& itrk);

    int GetNumberOfRefTracks();

    Double_t GetMaxChi2ndf() { return tag->GetMaxChi2ndf(); }
    Double_t GetClsLimMdist() { return tag->GetClsLimMdist(); }

  private:

    static TChain *tree; // input tree
    static TFile *out; // output file
    static TTree *otree; // output tree

    static TagMapsBasic *s1; // Tagger 1
    static TagMapsBasic *s2; // Tagger 2

    static RefCounter *cnt_s1; // Reference counter 1
    static RefCounter *cnt_s2; // Reference counter 2

    static Long64_t iev; // event number

    static TagMapsBasic *tag; // active tagger
    static RefCounter *cnt; // active reference counter

    static int min_ntrk; // minimal number of tracks in event
    static int min_ncls; // minimal number of clusters on all planes in event
    static int min_ncnt; // minimal number of reference tracks in event
    static int min_etrk; // minimal number of excess tracks as reconstructed tracks - reference tracks

};



#endif

