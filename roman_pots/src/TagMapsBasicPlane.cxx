
//_____________________________________________________________________________
//
// Tagger station composed of MAPS basic planes
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>
#include <map>

//ROOT
#include "TTree.h"
#include "TMath.h"

//Geant
#include "G4String.hh"

//local classes
#include "GeoParser.h"
#include "TagMapsBasicPlane.h"

using namespace std;

//_____________________________________________________________________________
TagMapsBasicPlane::TagMapsBasicPlane(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree):
    fNam(nam), fEmin(0.4), fTree(0), fEvtTree(evt_tree), fNhit(0), fClsMinLimMdist(0) {

  //connect the hits for the plane
  fHits.ConnectInput("lowQ2_"+fNam, tree);
  fHits.LocalFromGeo("vac_B2Q3", geo);

  //correct for local plane position inside its volume
  fHits.SetXPos( fHits.GetXPos() + geo->GetD("lowQ2_"+fNam, "xpos") );

  //cout << fNam << " xpos (mm): " << fHits.GetXPos() << endl;

}//TagMapsBasicPlane

//_____________________________________________________________________________
void TagMapsBasicPlane::ProcessEvent() {

  //process hits for current event

  LoadHits();
  fCls.clear();

  //if( GetHitsCount() < 12 ) return;

  //cout << fNam << " hits: " << GetHitsCount() << endl;

  //hits loop
  while(GetHitsCount() > 0) {

    //hit with most energy deposition as a seed for the cluster
    unsigned long ih = FindHitEmax();
    fHitStat[ih] = false; // mark the hit as used

    //initialize the cluster to the seed
    fCls.push_back(Cluster());
    Cluster& cls = fCls.back();
    cls.hits.push_back(ih);

    //MC track and pdg from the seed hit
    const TrkMapsBasicHits::Hit& seed_hit = fHits.GetHit( ih );
    cls.itrk = seed_hit.itrk;
    cls.pdg = seed_hit.pdg;

    //adjacent hits for the hit with the most energy
    int nfound = FindAdjHits(ih, cls.hits);

    //search for adjacent hits from the first set
    list<unsigned long> adj_hits_sec;
    do {
      nfound = 0;
      adj_hits_sec.clear();

      for(list<unsigned long>::iterator ith = cls.hits.begin(); ith != cls.hits.end(); ith++) {

        nfound += FindAdjHits(*ith, adj_hits_sec);
      }

      //append the next set of adjacent hits to the cluster hits
      for(list<unsigned long>::iterator ith = adj_hits_sec.begin(); ith != adj_hits_sec.end(); ith++) {
        cls.hits.push_back(*ith);
      }

    } while( nfound > 0 );

    //test for uniform gradient in cluster hits
    GradientTest(cls);

  }//hits loop

  fNCls = 0;
  fNClsPrim = 0;

  //clusters loop
  Int_t cls_id = 0;
  for(vector<Cluster>::iterator icls = fCls.begin(); icls != fCls.end(); icls++) {
    Cluster& cls = *icls;
    cls.id = cls_id++; // set the cluster ID

    //number of hits in the cluster
    cls.nhits = cls.hits.size();

    //cluster position by energy-weighted average
    for(list<unsigned long>::iterator ith = cls.hits.begin(); ith != cls.hits.end(); ith++) {
      const TrkMapsBasicHits::Hit& hit = fHits.GetHit( *ith );

      cls.en += hit.en;
      cls.x += hit.x*hit.en;
      cls.y += hit.y*hit.en;

      cls.is_prim = cls.is_prim && hit.is_prim;

      cls.sigma_x += hit.en*hit.x*hit.x;
      cls.sigma_y += hit.en*hit.y*hit.y;
    }

    cls.x = cls.x/cls.en;
    cls.y = cls.y/cls.en;

    cls.sigma_x = cls.GetSigma(cls.sigma_x, cls.x);
    cls.sigma_y = cls.GetSigma(cls.sigma_y, cls.y);

    //if(cls.nhits > 4) {
      //cout << fNam << " " << cls.nhits << endl;
      //PrintCluster(cls);
    //}

    //if(cls.nhits > 1) {
      //cout << cls.nhits << " " << cls.x << " " << cls.y << " " << cls.en << " " << cls.is_prim << " ";
      //cout << cls.nhits << " " << cls.x << " " << cls.y << " " << cls.sigma_x << " " << cls.sigma_y << endl;
    //}

    //increment event counters
    fNCls++;
    if( cls.is_prim ) fNClsPrim++;

  }//clusters loop

  //cluster mutual distances and status
  for(vector<Cluster>::iterator icls = fCls.begin(); icls != fCls.end(); icls++) {
    Cluster& cls = *icls;

    //inner loop
    for(vector<Cluster>::iterator i2 = fCls.begin(); i2 != fCls.end(); i2++) {
      if( icls == i2 ) continue; // same cluster

      Cluster& cls2 = *i2;

      //distance between the clusters
      Double_t dist = TMath::Sqrt( (cls.x-cls2.x)*(cls.x-cls2.x) + (cls.y-cls2.y)*(cls.y-cls2.y) );

      //update the minimal distance for the cluster
      if( dist < cls.min_dist or cls.min_dist < 0 ) cls.min_dist = dist;

    }//inner loop

    //cluster status
    if( cls.min_dist > 0 and cls.min_dist < fClsMinLimMdist ) cls.stat = kFALSE; // limit on minimal distance to another cluster

  }//cluster mutual distances and status

  //cout << fNam << " clusters: " << fNCls << " " << fNClsPrim << endl;

}//ProcessEvent

//_____________________________________________________________________________
int TagMapsBasicPlane::FindAdjHits(unsigned long ih, list<unsigned long>& adj_hits) {

  //find hits adjacent to a hit at a given ih
  //along pixel and row direction

  const TrkMapsBasicHits::Hit& hit_start = fHits.GetHit(ih);
  Int_t ipix_start = hit_start.ipix;
  Int_t irow_start = hit_start.irow;

  //range in pixel and row indices for adjacent hits
  Int_t pmin = ipix_start-1;
  Int_t pmax = ipix_start+1;
  Int_t rmin = irow_start-1;
  Int_t rmax = irow_start+1;

  //counter for found hits
  int nfound = 0;

  for(unsigned long ihit=0; ihit<fHits.GetNhits(); ihit++) {
    if( !fHitStat[ihit] ) continue;

    //hit indices
    const TrkMapsBasicHits::Hit& hit = fHits.GetHit(ihit);
    Int_t ipix = hit.ipix;
    Int_t irow = hit.irow;

    //apply the range for adjacent hit
    if( ipix < pmin or ipix > pmax ) continue;
    if( irow < rmin or irow > rmax ) continue;

    //adjacent hit found
    adj_hits.push_back(ihit);

    //mark the hit as used
    fHitStat[ihit] = false;

    nfound++;

  }

  return nfound;

}//FindAdjHits

//_____________________________________________________________________________
unsigned long TagMapsBasicPlane::FindHitEmax() {

  //hit with most energy deposition

  //initial values
  unsigned long ih = 0;
  Double_t en = -1.;

  //compare to all other hits
  for(unsigned long ihit=0; ihit<fHits.GetNhits(); ihit++) {
    if( !fHitStat[ihit] ) continue;

    const TrkMapsBasicHits::Hit& hit = fHits.GetHit(ihit);

    if( hit.en < en ) continue;

    //update for hit at larger energy
    en = hit.en;
    ih = ihit;

  }

  return ih;

}//FindHitEmax

//_____________________________________________________________________________
int TagMapsBasicPlane::GetHitsCount() {

  //count hits with active status

  int nhit = 0;
  for(unsigned long ihit=0; ihit<fHitStat.size(); ihit++) {

    if( fHitStat[ihit] ) nhit++;
  }

  return nhit;

}//GetHitsCount

//_____________________________________________________________________________
void TagMapsBasicPlane::GradientTest(Cluster& cls) {

  //test hits in cluster for decreasing gradient from the seed
  //and remove those hits which would cause an increase in the gradient

  //cout << fNam << " grad test: " << cls.is_prim << " " << cls.nhits;
  //cout << " " << cls.x << " " << cls.y << endl;

  //seed hit for the cluster
  const TrkMapsBasicHits::Hit& seed_hit = fHits.GetHit( cls.hits.front() );

  list<unsigned long> hits_to_remove;

  //hit loop
  for(list<unsigned long>::iterator ith = cls.hits.begin(); ith != cls.hits.end(); ith++) {
    const TrkMapsBasicHits::Hit& hit = fHits.GetHit( *ith );

    //distance to the seed
    Int_t dx = seed_hit.ipix-hit.ipix;
    Int_t dy = seed_hit.irow-hit.irow;

    //adjacent hits over two or more pixels
    if( labs(dx) < 2 and labs(dy) < 2 ) continue;

    //direction to the seed in x and y
    Int_t dxy[2] = {0, 0};
    if( dx != 0 ) dxy[0] = dx>0?1:-1;
    if( dy != 0 ) dxy[1] = dy>0?1:-1;

    //cout << "  hit: " << hit.ipix << " " << hit.irow;
    //cout << " " << Form("%.0f", hit.en) << " " << hit.is_prim;
    //cout << " Dx: " << dx << " Dy: " << dy << " dxy: " << dxy[0] << " " << dxy[1] << endl;

    //hit status to satisfy the gradient, true = keep, false = remove from the cluster
    bool grad_stat = false;

    //all hits in the direction to the seed by a unit distance
    for(auto ihs = cls.hits.begin(); ihs != cls.hits.end(); ihs++) {
      const TrkMapsBasicHits::Hit& hit_to_seed = fHits.GetHit( *ihs );
      if( labs(hit_to_seed.ipix-hit.ipix) > 1 or labs(hit_to_seed.irow-hit.irow) > 1 ) continue; //unit distance
      if( hit_to_seed.ipix == hit.ipix and hit_to_seed.irow == hit.irow ) continue; //same hit

      //hit is in the direction to seed by dxy
      if( hit.ipix+dxy[0] != hit_to_seed.ipix and hit.irow+dxy[1] != hit_to_seed.irow ) continue;

      //cout << "    hit_to_seed: " << Form("%.0f", hit_to_seed.en) << endl;

      //hit of larger energy in the direction to the seed
      if( hit_to_seed.en > hit.en ) grad_stat = true;
    }

    //cout << "    grad_stat: " << grad_stat << endl;

    //keep the hits satisfying the gradient
    if( grad_stat ) continue;

    //cout << "    to remove: " << Form("%.0f", hit.en) << endl;

    //remove the hit not in gradient and all hits in the direction away from the seed
    for(auto ihs = cls.hits.begin(); ihs != cls.hits.end(); ihs++) {
      const TrkMapsBasicHits::Hit& hit_from_seed = fHits.GetHit( *ihs );
      if( hit_from_seed.ipix == hit.ipix and hit_from_seed.irow == hit.irow ) continue; //same hit

      //unit distance about the seed
      if( labs(hit_from_seed.ipix-seed_hit.ipix) < 2
        and labs(hit_from_seed.irow-seed_hit.irow) < 2 ) continue;

      //direction from the hit not in gradient
      Int_t gdx = SignI( hit_from_seed.ipix - hit.ipix );
      Int_t gdy = SignI( hit_from_seed.irow - hit.irow );

      //cout << "    hit_from_seed: " << Form("%.0f", hit_from_seed.en) << " ";
      //cout << gdx << " " << gdy << " " << dxy[0] << " " << dxy[1] << endl;

      //diagonal direction
      if( (labs(dxy[0]) + labs(dxy[1])) > 1 ) {
        if( dxy[0] == gdx ) continue;
        if( dxy[1] == gdy ) continue;
      }

      //direction along x or y
      if( dxy[0] == 0 ) {
        if( gdy == 0 ) continue;
        if( dxy[1] == gdy ) continue;
      }
      if( dxy[1] == 0 ) {
        if( gdx == 0 ) continue;
        if( dxy[0] == gdx ) continue;
      }

      //cout << "    remove hit_from_seed: " << Form("%.0f", hit_from_seed.en) << " ";
      //cout << gdx << " " << gdy << " " << dxy[0] << " " << dxy[1] << endl;

      //remove the hit, direction away from the seed
      hits_to_remove.push_back( *ihs );
    }

    //remove the original hit not in gradient
    hits_to_remove.push_back( *ith );

  }//hit loop

  //removing the hits from the cluster
  for(list<unsigned long>::iterator ith = hits_to_remove.begin(); ith != hits_to_remove.end(); ith++) {

    cls.hits.remove( *ith );
    fHitStat[ *ith ] = true;
  }

}//GradientTest

//_____________________________________________________________________________
void TagMapsBasicPlane::LoadHits() {

  //set initial status for all hits based on selection criteria

  //load hits for current event in input tree
  fHits.LoadHits();
  fHits.GlobalToLocal();

  //clear the status flags
  fHitStat.clear();

  //hit counters
  fNhit = 0;
  fNhitPrim = 0;

  //fNsel = 0;

  //hits loop
  for(unsigned long ihit=0; ihit<fHits.GetNhits(); ihit++) {

    //get the hit
    const TrkMapsBasicHits::Hit& hit = fHits.GetHit(ihit);

    //create status entry for the hit
    map<unsigned long, bool>::iterator istat = fHitStat.insert( make_pair(ihit, false) ).first;

    //energy threshold
    if( hit.en < fEmin ) continue;

    //mark hit as accepted
    (*istat).second = true;
    //fNsel++;

    //set the hit outputs
    fNhit++;

    fX = hit.x;
    fY = hit.y;
    fZ = hit.z;
    fE = hit.en;

    fPdg = hit.pdg;
    fId = hit.itrk;

    if( hit.is_prim ) fNhitPrim++;

    //cout << fNam << ": " << hit.pdg << " " << hit.x << " " << hit.y << " " << hit.z << " " << hit.en << endl;

    //fill the hit output for the layer
    if(fTree) fTree->Fill();

  }//hits loop

}//LoadHits

//_____________________________________________________________________________
void TagMapsBasicPlane::CreateOutput() {

  //output for the layer
  fTree = new TTree(fNam.c_str(), fNam.c_str());
  fTree->Branch("x", &fX, "x/D");
  fTree->Branch("y", &fY, "y/D");
  fTree->Branch("z", &fZ, "z/D");
  fTree->Branch("en", &fE, "en/D");
  fTree->Branch("pdg", &fPdg, "pdg/I");
  fTree->Branch("id", &fId, "id/I");

  //clusters tree
  fClsTree = new TTree((fNam+"_clusters").c_str(), (fNam+"_clusters").c_str());
  fClsTree->Branch("x", &fClsX, "x/D");
  fClsTree->Branch("y", &fClsY, "y/D");
  fClsTree->Branch("en", &fClsE, "en/D");
  fClsTree->Branch("nhits", &fClsNhits, "nhits/I");
  fClsTree->Branch("is_prim", &fClsPrim, "is_prim/O");
  fClsTree->Branch("sigma_x", &fClsSigX, "sigma_x/D");
  fClsTree->Branch("sigma_y", &fClsSigY, "sigma_y/D");
  fClsTree->Branch("ntrk", &fClsNtrk, "ntrk/I");
  fClsTree->Branch("min_dist", &fClsMinDist, "min_dist/D");

  //event tree
  fEvtTree->Branch((fNam+"_nhit").c_str(), &fNhit, (fNam+"_nhit/I").c_str());
  fEvtTree->Branch((fNam+"_nhit_prim").c_str(), &fNhitPrim, (fNam+"_nhit_prim/I").c_str());
  fEvtTree->Branch((fNam+"_ncls").c_str(), &fNCls, (fNam+"_ncls/I").c_str());
  fEvtTree->Branch((fNam+"_ncls_prim").c_str(), &fNClsPrim, (fNam+"_ncls_prim/I").c_str());

}//CreateOutput

//_____________________________________________________________________________
void TagMapsBasicPlane::FinishEvent() {

  //clusters loop
  for(vector<Cluster>::iterator icls = fCls.begin(); icls != fCls.end(); icls++) {
    Cluster& cls = *icls;

    //fill output on clusters
    fClsX = cls.x;
    fClsY = cls.y;
    fClsE = cls.en;
    fClsNhits = cls.nhits;
    fClsPrim = cls.is_prim;
    fClsSigX = cls.sigma_x;
    fClsSigY = cls.sigma_y;
    fClsNtrk = cls.ntrk;
    fClsMinDist = cls.min_dist;

    fClsTree->Fill();

  }//clusters loop

}//FinishEvent

//_____________________________________________________________________________
void TagMapsBasicPlane::WriteOutputs() {

  if(!fTree) return;

  cout << "Plane " << fNam << ", hits: " << fTree->GetEntries() << ", clusters: " << fClsTree->GetEntries() << endl;
  fTree->Write();
  fClsTree->Write();

}//WriteOutputs

//_____________________________________________________________________________
Double_t TagMapsBasicPlane::Cluster::GetSigma(Double_t swx2, Double_t pos) {

  //Bevington, Robinson, eq. 4.22, p. 58

  if( hits.size() < 2 ) return 0;

  Double_t sig2 = ((swx2/en) - pos*pos)/(hits.size() - 1);

  if(sig2 > 0) return TMath::Sqrt(sig2);

  return 0;

}//Cluster::GetSigma

//_____________________________________________________________________________
void TagMapsBasicPlane::PrintCluster(Cluster& cls) {

  //print cluster parameters

  cout << fNam << " cluster: " << cls.is_prim << " " << cls.nhits;
  cout << " " << cls.x << " " << cls.y << endl;

  //hit loop
  for(list<unsigned long>::iterator ith = cls.hits.begin(); ith != cls.hits.end(); ith++) {
    const TrkMapsBasicHits::Hit& hit = fHits.GetHit( *ith );

    cout << "  hit: " << hit.ipix << " " << hit.irow;// << " " << hit.x << " " << hit.y;
    cout << " " << Form("%.0f", hit.en) << " " << hit.is_prim;

    if(ith != cls.hits.begin()) {
      const TrkMapsBasicHits::Hit& seed_hit = fHits.GetHit( cls.hits.front() );

      cout << " Dx: " << seed_hit.ipix-hit.ipix;// << " " << seed_hit.x-hit.x;
      cout << " Dy: " << seed_hit.irow-hit.irow;// << " " << seed_hit.y-hit.y;
    }

    cout << endl;

  }//hit loop

}//PrintCluster


















