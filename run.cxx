
//C++ headers
#include <iostream>
#include <string>
#include <boost/program_options.hpp>

//explicit instantiation to reduce warnings from old Geant 4.10.00 on EIC nodes
template std::vector<std::basic_string<char> > boost::program_options::to_internal(const std::vector<std::basic_string<char> >&);

//Geant headers
#include "G4UIExecutive.hh"
#include "Randomize.hh"
#include "G4RunManager.hh"
#include "G4VisExecutive.hh"
#include "G4UImanager.hh"
#include "FTFP_BERT.hh"
#include "FTFP_BERT_HP.hh"
#include "G4OpticalPhysics.hh"

//local headers
#include "DetectorConstruction.h"
#include "ActionInitialization.h"

namespace po = boost::program_options;
using namespace std;

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //command line arguments
  po::options_description opt("Program arguments");
  opt.add_options()("vis", po::value<string>(), "visualization macro");
  opt.add_options()("mac,m", po::value<string>(), "batch macro");
  opt.add_options()("seed,s", po::value<long>(), "random seed");

  //parse the arguments
  po::variables_map opt_map;
  po::store(po::parse_command_line(argc, argv, opt), opt_map);

  //visualization macro
  G4String vis_mac("init_vis.mac"); // default name
  if(opt_map.count("vis")) {
    //name from the argument
    vis_mac = G4String( opt_map["vis"].as<string>() );
  }
  //batch macro
  G4String macro;
  if(opt_map.count("mac")) {
    macro = G4String( opt_map["mac"].as<string>() );
  }
  //random seed
  long random_seed = 0;
  if(opt_map.count("seed")) {
    random_seed = opt_map["seed"].as<long>();
  }

  //UI session
  G4String session;
  G4UIExecutive *ui = 0x0;
  if( !macro.size() ) {
    ui = new G4UIExecutive(argc, argv, session);
  }

  //random engine
  G4Random::setTheEngine(new CLHEP::RanecuEngine);

  //random seed
  G4cout << "Input seed: " << random_seed << G4endl;;
  G4Random::setTheSeed(random_seed);
  G4cout << "Start seed: " << G4Random::getTheSeed() << G4endl;

  //default run manager
  G4RunManager *runManager = new G4RunManager;

  //detector construction
  runManager->SetUserInitialization(new DetectorConstruction);

  //physics
  //FTFP_BERT *physicsList = new FTFP_BERT;
  FTFP_BERT_HP *physicsList = new FTFP_BERT_HP;
  //G4OpticalPhysics *optics = new G4OpticalPhysics();
  //physicsList->RegisterPhysics(optics); // uncomment to turn optics on
  runManager->SetUserInitialization(physicsList);

  //action
  runManager->SetUserInitialization(new ActionInitialization);

  //visualization
  G4VisExecutive *visManager = new G4VisExecutive;
  visManager->Initialize();

  //user interface manager
  G4UImanager *UImanager = G4UImanager::GetUIpointer();

  //UI session for interactive or batch mode
  G4String command = "/control/execute ";
  if ( macro.size() > 0 ) {
    // batch mode
    UImanager->ApplyCommand(command+macro);
  } else {
    //interactive
    UImanager->ApplyCommand(command+vis_mac);
    if (ui->IsGUI()) {
      UImanager->ApplyCommand("/control/execute gui.mac");
    }
    ui->SessionStart();
    delete ui;
  }

  //job termination
  delete visManager;
  delete runManager;

  return 0;

}//main





























