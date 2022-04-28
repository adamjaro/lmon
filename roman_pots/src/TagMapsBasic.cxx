
//_____________________________________________________________________________
//
// Tagger station composed of MAPS basic planes
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>

//ROOT
#include "TTree.h"

//Geant
#include "G4String.hh"

//local classes
#include "TagMapsBasicPlane.h"
#include "TagMapsBasic.h"

using namespace std;

//_____________________________________________________________________________
TagMapsBasic::TagMapsBasic(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree):
    fNam(nam) {

  //planes for the station, A, B and C
  fPlanes.push_back( new TagMapsBasicPlane(fNam+"A", tree, geo, evt_tree) );
  fPlanes.push_back( new TagMapsBasicPlane(fNam+"B", tree, geo, evt_tree) );
  fPlanes.push_back( new TagMapsBasicPlane(fNam+"C", tree, geo, evt_tree) );

}//TagMapsBasic

//_____________________________________________________________________________
void TagMapsBasic::ProcessEvent() {

  //process event for individual planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::ProcessEvent ));

}//ProcessEvent

//_____________________________________________________________________________
void TagMapsBasic::CreateOutput() {

  //create output for individual planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::CreateOutput ));

}//CreateOutput

//_____________________________________________________________________________
void TagMapsBasic::WriteOutputs() {

  //write outputs for the planes
  for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &TagMapsBasicPlane::WriteOutputs ));

}//WriteOutputs

















