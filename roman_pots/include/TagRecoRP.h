
#ifndef TagRecoRP_h
#define TagRecoRP_h

// Reconstruction for Roman Pot tagger station

class TH1D;

class TagRecoRP {

  public:

    TagRecoRP(std::string nam, boost::program_options::options_description *opt);

    void Initialize(boost::program_options::variables_map *opt_map);
    void Import(TFile *in);

    void AddInput(Double_t x, Double_t y, Double_t theta_x, Double_t theta_y, Double_t en, Double_t theta, Double_t phi);
    void Export();

    void CreateRecoOutput();
    void AddOutputBranch(std::string nam, Double_t *val);
    bool Reconstruct(Double_t x, Double_t y, Double_t theta_x, Double_t theta_y);
    void WriteRecoOutput() { fRecTree->Write(); }

  private:

    template<typename T> void AddOpt(std::string onam, boost::program_options::options_description *opt);
    template<typename T> T GetOpt(std::string onam, boost::program_options::variables_map *opt_map);

    std::string fNam; // station name

    //range and segmentation in tagger parameters
    TH1D *fHX; // x position, mm
    TH1D *fHY; // y position, mm
    TH1D *fHThetaX; // theta_x angle, rad
    TH1D *fHThetaY; // theta_y angle, rad

    //link from tagger quantities to electron kinematics
    class Link {
      public:

      Link(): en(0), theta(0), phi(0) {}

      Double_t en; // electron energy, GeV
      Double_t theta; // electron polar angle, rad
      Double_t phi; // electron azimuthal angle, rad

      void AddElectron(double e, double t, double p);

      void Evaluate();

      unsigned int GetNinp() { return fEn.size(); }

      private:

      Double_t GetMean(std::vector<double>& v);

      std::vector<double> fEn; // inputs in energy, GeV
      std::vector<double> fTheta; // inputs in theta, rad
      std::vector<double> fPhi; // inputs in phi, rad

    };//Link

    std::map<std::vector<int>, Link> fLinks; // links from tagger to electrons

    //reconstruction tree
    TTree *fRecTree;
    Double_t rec_el_E; // reconstructed energy, GeV
    Double_t rec_el_theta; // reconstructed polar angle, rad
    Double_t rec_el_phi; // reconstructed azimuthal angle, rad
    Double_t rec_Q2; // reconstructed Q^2, GeV^2

};

#endif










