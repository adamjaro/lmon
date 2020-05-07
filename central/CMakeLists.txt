
#central library
set (CEN_LIB central)

#BeAST solenoid
list(APPEND EXTRA_INCLUDES "$ENV{HOME}/sim/magnetic_field/BeastMagneticField/install/include")
list(APPEND EXTRA_LIBS bmf)

#local include
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

#sources and headers for central library
file(GLOB central_sources ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cxx)
file(GLOB central_headers ${CMAKE_CURRENT_SOURCE_DIR}/include/*.h)

#make the central library
add_library (${CEN_LIB} SHARED ${central_sources} ${central_headers})
target_include_directories(${CEN_LIB} PUBLIC ${EXTRA_INCLUDES})
target_link_libraries(${CEN_LIB} ${Geant4_LIBRARIES} ${ROOT_DEPS} ${EXTRA_LIBS})

