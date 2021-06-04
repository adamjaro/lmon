
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(lmon)

cmake_policy(SET CMP0054 NEW)

#shared library
set (LIB lmonBase)

#executable
set (BIN run_lmon)

#Geant
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})

#local include
include_directories(${PROJECT_SOURCE_DIR}/include)

#sources and headers
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cxx)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.h)

#BOOST
find_package(Boost COMPONENTS program_options REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

#ROOT
find_package(ROOT REQUIRED COMPONENTS Core EG Hist Physics RIO Tree MathCore)
include(${ROOT_USE_FILE})

#dictionary for detectors
set (DICT G__DET.cxx)
ROOT_GENERATE_DICTIONARY(G__DET Detector.h SensDetDummy.h ExitWinZEUS.h LINKDEF include/LinkDef.h)

#component libraries
set(COMPONENT_LIBS)
set(COMPONENT_INCLUDE)

#central detector
option(BUILD_CENTRAL "Build central detector" OFF)
set(BEAST_INSTALL "$ENV{HOME}/sim/magnetic_field/BeastMagneticField/install" CACHE PATH "BeAST solenoid field")
configure_file(include/central_config.h.in central_config.h)
if(BUILD_CENTRAL)
  add_subdirectory(central)
  link_directories(${BEAST_INSTALL}/lib)
endif()

#calorimeter set
add_subdirectory(calo)

#base shared library
#add_library (${LIB} SHARED ${sources} ${headers} ${DICT})
add_library (${LIB} SHARED ${sources} ${headers})
target_include_directories(${LIB} PUBLIC "${CMAKE_CURRENT_BINARY_DIR}" ${COMPONENT_INCLUDE})
target_link_libraries(${LIB} ${Geant4_LIBRARIES} ${ROOT_LIBRARIES})

#binary executable
add_executable(${BIN} run.cxx)
target_link_libraries(${BIN} ${Geant4_LIBRARIES} ${LIB} ${Boost_LIBRARIES} ${COMPONENT_LIBS})















