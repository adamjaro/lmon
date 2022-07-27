
#ifndef AnaMapsBasic_h
#define AnaMapsBasic_h

class AnaMapsBasic {

  public:

    AnaMapsBasic() {}

    void Run(const char *conf);

  private:

    void AssociateMC(TagMapsBasic& tag, RefCounter& cnt);

    std::string GetStr(boost::program_options::variables_map& opt_map, std::string par);

};

extern "C" {

  AnaMapsBasic* make_AnaMapsBasic() { return new AnaMapsBasic(); }

  void run_AnaMapsBasic(AnaMapsBasic& t, const char *c) { t.Run(c); }

}

#endif

