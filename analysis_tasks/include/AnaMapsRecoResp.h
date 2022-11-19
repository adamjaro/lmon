
#ifndef AnaMapsRecoResp_h
#define AnaMapsRecoResp_h

#include "AnaMapsBasic.h"

class AnaMapsRecoResp : protected AnaMapsBasic {

  public:

    AnaMapsRecoResp(const char *conf);

  private:

    void ProcessEvent(TagMapsBasic& tag, RefCounter& cnt, EThetaPhiReco& rec);
    void WriteOutputs(TagMapsBasic& tag, RefCounter& cnt);

    //input true kinematics, assuming one generated electron per event
    Double_t true_el_E; // electron energy, GeV
    Double_t true_el_theta; // electron polar angle, rad
    Double_t true_el_phi; // electron azimuthal angle, rad

};

#endif

