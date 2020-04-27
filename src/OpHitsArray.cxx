
//_____________________________________________________________________________
//
// hits array for optical photon detector
//
//_____________________________________________________________________________

//C++
#include <map>
#include <vector>

//ROOT
#include "TTree.h"

//Geant
#include "G4ios.hh"

//local classes
#include "OpHitsArray.h"

using namespace std;

//_____________________________________________________________________________
OpHitsArray::OpHitsArray(G4double dt): fDt(dt) {

}//OpHitsArray

//_____________________________________________________________________________
void OpHitsArray::CreateOutput(std::string nam, TTree *tree) {

  //create output branches for the hits

  //G4cout << "OpHitsArray::CreateOutput, " << nam << " " << tree << G4endl;

  tree->Branch((nam+"_hits_time").c_str(), &fHitsTime);
  tree->Branch((nam+"_hits_nphot").c_str(), &fHitsNphot);

}//CreateOutput

//_____________________________________________________________________________
void OpHitsArray::Clear() {

  //clear the hits map and output vectors

  //G4cout << "OpHitsArray::Clear" << G4endl;

  fHits.clear();

  fHitsTime.clear();
  fHitsNphot.clear();

}//Clear

//_____________________________________________________________________________
void OpHitsArray::AddHit(G4double time) {

  //add hit to the array

  //time index in hit map
  int idt = int(floor(time/fDt));

  //pair<map<int, hit>::iterator, bool> ihit; // alternative approach with iterator
  //ihit = fHits.insert( make_pair(idt, hit(idt*fDt)) );
  //(*ihit.first).second.fNphot += 1;

  //create or update the hit
  fHits[idt].fTime = idt*fDt;
  fHits[idt].fNphot += 1;

  //G4cout << "OpHitsArray::AddHit, " << time << " " << fHits[idt].fTime << " " << fHits[idt].fNphot << G4endl;

}//AddHit

//_____________________________________________________________________________
void OpHitsArray::WriteOutput() {

  //load the output vectors from hits map

  //G4cout << "OpHitsArray::WriteOutput" << G4endl;

  map<int, hit>::iterator ihit = fHits.begin();

  //hits loop
  while(ihit != fHits.end()) {

    hit& ch = (*ihit).second;

    fHitsTime.push_back(ch.fTime);
    fHitsNphot.push_back(ch.fNphot);

    //G4cout << fHitsTime.back() << " " << fHitsNphot.back() << G4endl;

    ihit++;
  }//hits loop


}//WriteOutput
















