
#ifndef AnaPhotTime_h
#define AnaPhotTime_h

class AnaPhotTime {

  public:

    AnaPhotTime() {}

    void Run(const char*);

  private:

    std::string GetStr(boost::program_options::variables_map& opt_map, std::string par);

};

extern "C" {

  AnaPhotTime* make_AnaPhotTime() { return new AnaPhotTime(); }

  void run_AnaPhotTime(AnaPhotTime& t, const char *c) { t.Run(c); }

}

#endif

