
#ifndef AnaMapsRecoResp_h
#define AnaMapsRecoResp_h

#include "AnaMapsBasic.h"

class AnaMapsRecoResp : protected AnaMapsBasic {

  public:

    AnaMapsRecoResp(const char *conf);

  private:

    void ProcessEvent(TagMapsBasic& tag, RefCounter& cnt);
    void WriteOutputs(TagMapsBasic& tag, RefCounter& cnt);

};

#endif

