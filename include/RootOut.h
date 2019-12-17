#ifndef RootOut_h
#define RootOut_h

//helper class for ROOT TTree output

class TFile;
class TTree;

class RootOut {

  public:

    RootOut();

    bool Open(std::string nam); // open the output and create the tree
    void Close(); // write the tree and close outpu file

    TTree *GetTree() {return fDetTree;} // provide the tree to the detectors
    void FillTree(); // call fill for the tree

  private:

    TFile *fOut; // output file
    TTree *fDetTree; // output tree

};

#endif

