
#ifndef PhotoHitsV2Coll_h
#define PhotoHitsV2Coll_h

#include "DetectorData.h"

//hit representation
namespace PhotoHitsV2 {

  class Hit {
  public:

    //hit members to appear in fUnitIO
    Double_t pos_x; // hit position in x, mm
    Double_t pos_y; // hit position in y, mm
    Double_t pos_z; // hit position in z, mm
    Double_t time; // time of the hit, ns

  };//Hit
}//PhotoHitsV2

//hits collection
class PhotoHitsV2Coll : public DetectorData<PhotoHitsV2::Hit, std::vector<PhotoHitsV2::Hit>> {

  public:

    PhotoHitsV2Coll();

    //make new hit and return reference to it
    PhotoHitsV2::Hit& CreateHit() { fStorage.push_back(PhotoHitsV2::Hit()); return fStorage.back(); }

};//PhotoHitsV2Coll

#endif

