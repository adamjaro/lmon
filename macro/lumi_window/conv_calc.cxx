
//calculate the conversion probability

#if !defined(__CLING__) || defined(__ROOTCLING__)
//C++
#include <list>
#include <vector>
#include <iostream>

//ROOT
#include "TTree.h"
#include "TGraphAsymmErrors.h"
#include "TH1D.h"
#include "TMath.h"

//local functions
#include "get_bins.cxx"

using namespace std;

#endif

//_____________________________________________________________________________
class conv_calc {
  public:
  //_____________________________________________________________________________
  conv_calc(TTree *t, Double_t p, Double_t d): tree(t), prec(p), delt(d) {

    tree->SetBranchAddress("gen_en", &gen_en);
    tree->SetBranchAddress("conv", &conv);
    tree->SetBranchAddress("clean", &clean);

    nev = 0;

    conv_in_all = false;
    clean_in_sel = false;

  }//conv_calc

  //_____________________________________________________________________________
  TGraphAsymmErrors get_conv() {

    //number of events
    if(nev == 0) {
      nev = tree->GetEntriesFast();
    }

    list<Double_t> valAll, valSel;

    //tree loop
    for(ULong64_t iev=0; iev<nev; iev++) {
      tree->GetEntry(iev);

      //conversion in all events
      if(conv_in_all and !conv) {continue;}

      //all events
      valAll.push_back(gen_en);

      //conversion selection
      if(!conv) {continue;}

      //clean conversions in selected events
      if(clean_in_sel and !clean) {continue;}

      //cout << conv << " " << clean << endl;

      //selected events
      valSel.push_back(gen_en);

    }//tree loop

    //get the bins
    vector<Double_t> bins;
    get_bins(valAll, valSel, bins, prec, delt); // in get_bins.cxx

    //distributions for all and selected events
    TH1D hAll("hAll", "hAll", bins.size()-1, bins.data());
    TH1D hSel("hSel", "hSel", bins.size()-1, bins.data());
    h1_from_list(valAll, hAll); // in get_acc.C
    h1_from_list(valSel, hSel);

    //output conversion probability
    TGraphAsymmErrors conv(&hSel, &hAll);

    return conv;

  }//get_conv


  //input tree
  TTree *tree;
  Float_t gen_en;
  Bool_t conv;
  Bool_t clean;

  bool conv_in_all; // conversion in all events
  bool clean_in_sel; // clean conversion in selected events

  ULong64_t nev; // number of events
  Double_t prec; // precision
  Double_t delt; // delta for steps

};//conv_calc























