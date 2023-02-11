
#ifndef PhotoHitsV2_h
#define PhotoHitsV2_h

#include "DetectorData.h"

namespace PhotoHitsV2 {

//hit representation
struct Hit {

  //hit members to appear in fUnitIO
  Double_t pos_x; // hit position in x, mm
  Double_t pos_y; // hit position in y, mm
  Double_t pos_z; // hit position in z, mm
  Double_t time; // time of the hit, ns

};//Hit

//hits collection
class Coll : public DetectorData<Hit> {

  public:

    Coll();

    Hit& CreateHit();

};//Coll

}//PhotoHitsV2

#endif

