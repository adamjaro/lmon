
// compile and run for reader.C

//_____________________________________________________________________________
void run_reader() {

  //local include
  gROOT->ProcessLine(".include ../../include");

  //for EIC nodes
  gROOT->ProcessLine(".include /afs/rhic.bnl.gov/eic/PACKAGES/GEANT4.10/geant4.10.00-install/include/Geant4");

  //library with detector codes
  gSystem->Load("../../build/libdet.so");

  //run the macro
  gROOT->ProcessLine(".x reader.C+g");

}//run_reader

