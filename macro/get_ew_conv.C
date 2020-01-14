
//exit window conversion probability

//_____________________________________________________________________________
TGraphAsymmErrors get_ew_conv(TTree *tree, string bnam, string bmatch, Double_t prec, Double_t delt, Double_t mult=1, Double_t add=0) {

  //load tree values to the lists
  tree->SetBranchStatus("*", 0);
  tree->SetBranchStatus(bnam.c_str(), 1);
  tree->SetBranchStatus(bmatch.c_str(), 1);

  Double_t val; // value in the tree
  Bool_t mstat; // match status for a given value
  tree->SetBranchAddress(bnam.c_str(), &val);
  tree->SetBranchAddress(bmatch.c_str(), &mstat);

  //values for all and matched entries
  list<Double_t> valAll, valSel;

  //tree loop
  ULong64_t nent = tree->GetEntriesFast();
  //ULong64_t nent = 1200000;
  for(ULong64_t ient=0; ient<nent; ient++) {

    //load values
    tree->GetEntry(ient);

    //apply multiplicative and additive constants
    val = val*mult + add;

    //fill the lists
    valAll.push_back(val);
    if(mstat == 1) valSel.push_back(val);

  }//tree loop

  tree->ResetBranchAddresses();

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

  //bin edges
  vector<Double_t> bins;

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

  //for(UInt_t i=0; i<bins.size(); i++) {
    //cout << i << " " << bins[i] << endl;
  //}

  //values histograms using the bin edges
  TH1D hAll("hAll", "hAll", bins.size()-1, bins.data());
  TH1D hSel("hSel", "hSel", bins.size()-1, bins.data());
  hAll.Sumw2();
  hSel.Sumw2();

  //fill the histograms from the lists
  itAll = valAll.cbegin();
  while(itAll != valAll.cend()) {
    hAll.Fill(*itAll);
    itAll++;
  }
  itSel = valSel.cbegin();
  while(itSel != valSel.cend()) {
    hSel.Fill(*itSel);
    itSel++;
  }

  //output efficiency distribution
  TGraphAsymmErrors eff(&hSel, &hAll);

  //eff.SetPoint(0, 1e-3, 0.1);

  return eff;

}//get_ew_conv

















