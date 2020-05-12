
//_____________________________________________________________________________
TGraphAsymmErrors get_Q2_acc(TTree *tree, Double_t ebeam, Double_t theta_max, Double_t prec, Double_t delt, ULong64_t nev=0) {

  //connect the tree
  //tree->SetBranchStatus("*", 0);
  //tree->SetBranchStatus("el_gen", 1);
  //tree->SetBranchStatus("el_theta", 1);
  //tree->SetBranchStatus("lowQ2_IsHit", 1);

  Double_t el_gen, el_theta;
  Bool_t lowQ2_IsHit, lowQ2s1_IsHit, lowQ2s2_IsHit, ecal_IsHit;
  tree->SetBranchAddress("el_gen", &el_gen);
  tree->SetBranchAddress("el_theta", &el_theta);
  //tree->SetBranchAddress("lowQ2_IsHit", &lowQ2_IsHit);
  tree->SetBranchAddress("lowQ2s1_IsHit", &lowQ2s1_IsHit);
  tree->SetBranchAddress("lowQ2s2_IsHit", &lowQ2s2_IsHit);
  tree->SetBranchAddress("ecal_IsHit", &ecal_IsHit);

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
    valAll.push_back(lQ2);

    //selection for hit in the tagger and B2eR acceptance
    //if(lowQ2_IsHit != kTRUE || TMath::Pi()-el_theta > theta_max) {
    //if(lowQ2_IsHit != kTRUE) {
    //if(lowQ2s2_IsHit != kTRUE) {
    //if(lowQ2s1_IsHit != kTRUE and lowQ2s2_IsHit != kTRUE) {
    if(lowQ2s1_IsHit != kTRUE and lowQ2s2_IsHit != kTRUE and ecal_IsHit != kTRUE) {
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

}//get_Q2_acc






























