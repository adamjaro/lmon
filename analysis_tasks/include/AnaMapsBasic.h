
#ifndef AnaMapsBasic_h
#define AnaMapsBasic_h

class AnaMapsBasic {

  public:

    AnaMapsBasic() {}

    void Run(const char *conf);

  protected:

    void AssociateMC(TagMapsBasic& tag, RefCounter& cnt);

    std::string GetStr(boost::program_options::variables_map& opt_map, std::string par);

};



#endif

