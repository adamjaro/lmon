
#ifndef TagRecoRP_h
#define TagRecoRP_h

// Reconstruction for Roman Pot tagger station

class TH1D;

class TagRecoRP {

  public:

    TagRecoRP(std::string nam, boost::program_options::options_description *opt);

    void Initialize(boost::program_options::variables_map *opt_map);

    void AddInput(Double_t x, Double_t y, Double_t theta_x, Double_t theta_y);

    void WriteOutput();

  private:

    template<typename T> void AddOpt(std::string onam, boost::program_options::options_description *opt);
    template<typename T> T GetOpt(std::string onam, boost::program_options::variables_map *opt_map);

    std::string fNam; // station name

    //range and segmentation in tagger parameters
    TH1D *fHX; // x position, mm
    TH1D *fHY; // y position, mm
    TH1D *fHThetaX; // theta_x angle, rad
    TH1D *fHThetaY; // theta_y angle, rad

    //std::map

};

#endif

