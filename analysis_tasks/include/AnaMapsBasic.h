
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

    //input true kinematics
    //Double_t true_el_E;
    //Double_t true_el_theta;
    //Double_t true_el_phi;
    //Double_t true_Q2;

    static Double_t beam_en; // beam energy, GeV

};



#endif

