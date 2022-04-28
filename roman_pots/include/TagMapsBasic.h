
#ifndef TagMapsBasic_h
#define TagMapsBasic_h

// Tagger station composed of MAPS basic planes

class TagMapsBasicPlane;
class GeoParser;

class TagMapsBasic {

  public:

    TagMapsBasic(std::string nam, TTree *tree, GeoParser *geo, TTree *evt_tree);

    void ProcessEvent();

    void CreateOutput();
    void WriteOutputs();

  private:

    std::string fNam; // station name
    std::vector<TagMapsBasicPlane*> fPlanes; // planes for the station

};

#endif

