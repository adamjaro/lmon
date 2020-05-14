
//calculate the acceptance in log_10(Q^2)

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
#include "get_acc.C"

using namespace std;

#endif

//_____________________________________________________________________________
struct acc_Q2_calc {

  //_____________________________________________________________________________
  acc_Q2_calc(TTree *t, Double_t eb, Double_t p, Double_t d, ULong64_t n=0):
    tree(t), ebeam(eb), prec(p), delt(d), nev(n), lQ2min(9999), lQ2max(9999), sel_mode(1) {

    tree->SetBranchAddress("el_gen", &el_gen);
    tree->SetBranchAddress("el_theta", &el_theta);
    tree->SetBranchAddress("lowQ2s1_IsHit", &lowQ2s1_IsHit);
    tree->SetBranchAddress("lowQ2s2_IsHit", &lowQ2s2_IsHit);
    tree->SetBranchAddress("ecal_IsHit", &ecal_IsHit);

  }//acc_Q2_calc

  //_____________________________________________________________________________
  TGraphAsymmErrors get_acc() {

    //number of events
    if(nev == 0) {
      nev = tree->GetEntriesFast();
    }

    //log_10(Q^2) for all events and evens with hit in the tagger
    list<Double_t> valAll, valSel;

    //tree loop
    for(ULong64_t iev=0; iev<nev; iev++) {
      tree->GetEntry(iev);

      //obtain the log_10(Q^2)
      Double_t lQ2 = TMath::Log10(2.*ebeam*el_gen*(1.-TMath::Cos(TMath::Pi()-el_theta)));

      //select the lQ2 in range if requested
      if(lQ2min<9998 and lQ2 < lQ2min) continue;
      if(lQ2max<9998 and lQ2 > lQ2max) continue;

      valAll.push_back(lQ2);

      //selection for hit in the tagger

      if(sel_mode == 1 and lowQ2s1_IsHit != kTRUE) continue;
      if(sel_mode == 2 and lowQ2s2_IsHit != kTRUE) continue;
      if(sel_mode == 3 and lowQ2s1_IsHit != kTRUE and lowQ2s2_IsHit != kTRUE) continue;
      if(sel_mode == 4 and ecal_IsHit != kTRUE) continue;
      if(sel_mode == 5 and lowQ2s1_IsHit != kTRUE and lowQ2s2_IsHit != kTRUE and ecal_IsHit != kTRUE) {
        continue;
      }

      //selected log_10(Q^2)
      valSel.push_back(lQ2);

    }//tree loop

    //get the bins
    vector<Double_t> bins;
    get_bins(valAll, valSel, bins, prec, delt); // in get_acc.C

    //distributions for all and selected events
    TH1D hAll("hAll", "hAll", bins.size()-1, bins.data());
    TH1D hSel("hSel", "hSel", bins.size()-1, bins.data());
    h1_from_list(valAll, hAll); // in get_acc.C
    h1_from_list(valSel, hSel);

    //output acceptance distribution
    TGraphAsymmErrors acc(&hSel, &hAll);

    return acc;

  }//get_acc

  //_____________________________________________________________________________
  void release_tree() {

    tree->ResetBranchAddresses();

  }//release_tree

  //input tree
  TTree *tree;
  Double_t el_gen, el_theta;
  Bool_t lowQ2_IsHit, lowQ2s1_IsHit, lowQ2s2_IsHit, ecal_IsHit;

  Double_t ebeam; // beam energy

  Double_t prec; // precision
  Double_t delt; // delta for steps
  ULong64_t nev; // number of events

  Double_t lQ2min; // minimal log_10(Q^2)
  Double_t lQ2max; // maximal log_10(Q^2)

  Int_t sel_mode; // selection mode

};//acc_Q2_calc

















