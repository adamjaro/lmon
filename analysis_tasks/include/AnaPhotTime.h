
#ifndef AnaPhotTime_h
#define AnaPhotTime_h

class AnaPhotTime {

  public:

    AnaPhotTime() {}

    void Run(const char*);

  private:

};

extern "C" {

  AnaPhotTime* make_AnaPhotTime() { return new AnaPhotTime(); }

  void run_AnaPhotTime(AnaPhotTime& t, const char *c) { t.Run(c); }

}

#endif

