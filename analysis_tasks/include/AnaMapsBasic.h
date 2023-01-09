
#ifndef AnaMapsBasic_h
#define AnaMapsBasic_h

class EThetaPhiReco;

class AnaMapsBasic {

  public:

    AnaMapsBasic() {}

    void Run(const char *conf);

  protected:

    void AssociateMC(TagMapsBasic& tag, RefCounter& cnt);

    std::string GetStr(boost::program_options::variables_map& opt_map, std::string par);

  private:

    void ElectronRec(TagMapsBasic& tag, RefCounter&, EThetaPhiReco *rec);

    Double_t beam_en; // beam energy, GeV

};



#endif

