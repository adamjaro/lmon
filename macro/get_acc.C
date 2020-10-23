
//spectrometer acceptance

void get_bins(list<Double_t>&, list<Double_t>&, vector<Double_t>&, Double_t, Double_t);
void tree_to_list(TTree*, list<Double_t>&, string);

//_____________________________________________________________________________
TGraphAsymmErrors get_acc(TTree *tree, string bnam, string sel, Double_t prec, Double_t delt) {

  //tree satisfying selection 'sel'
  //TTree *treeSel = tree->CopyTree(sel.c_str(), "", 30000);
  TTree *treeSel = tree->CopyTree(sel.c_str());

  cout << tree->GetEntries() << endl;
  cout << treeSel->GetEntries() << endl;

  //values for all and matched entries
  list<Double_t> valAll, valSel;
  tree_to_list(tree, valAll, bnam);
  tree_to_list(treeSel, valSel, bnam);
  delete treeSel;

  //bin edges
  vector<Double_t> bins;
  get_bins(valAll, valSel, bins, prec, delt);

  //values histograms using the bin edges
  TH1D hAll("hAll", "hAll", bins.size()-1, bins.data());
  TH1D hSel("hSel", "hSel", bins.size()-1, bins.data());
  hAll.Sumw2();
  hSel.Sumw2();

  tree->Draw((bnam+" >> hSel").c_str(), sel.c_str());
  tree->Draw((bnam+" >> hAll").c_str());

  //output acceptance distribution
  TGraphAsymmErrors acc(&hSel, &hAll);

  return acc;

}//get_acc

//_____________________________________________________________________________
void get_bins(list<Double_t> &valAll, list<Double_t> &valSel, vector<Double_t> &bins, Double_t prec, Double_t delt) {

  //get bin edges for the input lists

  //sort the lists
  valAll.sort();
  valSel.sort();

  //range for bin edges
  Double_t minval = *(valSel.cbegin());
  Double_t maxval = *(valSel.crbegin());
  cout << "Range for bin edges: " << minval << " " << maxval << endl;

  //move both lists to the start of the range
  list<Double_t>::const_iterator itAll = valAll.cbegin();
  list<Double_t>::const_iterator itSel = valSel.cbegin();
  while( *itAll < minval ) itAll++;
  while( *itSel < minval ) itSel++;

  //starting edge
  bins.push_back(minval);

  //initialize the counters and current maximum
  UInt_t nsel = 0;
  UInt_t nall = 0;
  Double_t cmax = minval + delt;
  //find bin edges
  while(1) {
    //move to the current limit
    while( itSel != valSel.cend() and *itSel < cmax ) {
      nsel++;
      itSel++;
    }
    while( itAll != valAll.cend() and *itAll < cmax ) {
      nall++;
      itAll++;
    }

    //cout << nsel << " " << nall << endl;

    //relative Binomial error
    Double_t rel = 1.;
    if( nsel != 0 and nall != 0 and nsel != nall) {
      Double_t xsel = Double_t(nsel);
      Double_t xall = Double_t(nall);
      rel = TMath::Sqrt( (xall-xsel)/(xall*xsel) );
      //if( xsel/xall < ons ) rel = rel/2.;
    }

    //cout << "rel: " << rel << endl;

    //test for maximal allowed error
    if( rel < prec ) {
      //bin edge found, max relative error satisfied
      bins.push_back(cmax);
      //reset the counters for next bin
      nall = 0;
      nsel = 0;
      cout << "bin edge: " << cmax << endl;
    }

    //increment the current limit
    cmax += delt;

    //test for end of momenta interval
    if( cmax > maxval ) {
      //set last found edge to the end of values interval and finish
      //bins[bins.size()-1] = maxval;
      bins.push_back(maxval);
      break;
    }

  }//find bin edges

}//get_bins

//_____________________________________________________________________________
void tree_to_list(TTree *tree, list<Double_t> &list, string bnam) {

  //load tree branch bnam to a list

  tree->SetBranchStatus("*", 0);
  tree->SetBranchStatus(bnam.c_str(), 1);

  Double_t val; // value in the tree
  tree->SetBranchAddress(bnam.c_str(), &val);

  //tree loop
  ULong64_t nent = tree->GetEntriesFast();
  //ULong64_t nent = 12;
  for(ULong64_t ient=0; ient<nent; ient++) {

    tree->GetEntry(ient);
    list.push_back(val);

    //cout << val << endl;

  }//tree loop

  tree->ResetBranchAddresses();
  tree->SetBranchStatus("*", 1);

}//tree_to_list

//_____________________________________________________________________________
void h1_from_list(list<Double_t> &inp, TH1D &hx) {

  //fill a TH1D histogram from the input list
  hx.Sumw2();

  //list loop
  list<Double_t>::const_iterator it = inp.cbegin();
  while(it != inp.cend()) {
    hx.Fill(*it);
    it++;
  }//list loop

}//h1_from_list

//_____________________________________________________________________________
TH1D h1_from_list(string nam, list<Double_t>& inp, vector<Double_t>& bins) {

  //create TH1D from input list
  TH1D hx(nam.c_str(), nam.c_str(), bins.size()-1, bins.data());

  h1_from_list(inp, hx);

  return hx;

}//h1_from_list














