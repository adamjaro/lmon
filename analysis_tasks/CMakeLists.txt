
#local library
set(ANA_LIB lmonAnalysisTasks)

#sources and headers for the tasks
file(GLOB det_src ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cxx)
file(GLOB det_inc ${CMAKE_CURRENT_SOURCE_DIR}/include/*.h)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

#build the tasks library
add_library (${ANA_LIB} SHARED ${det_src} ${det_inc})
target_link_libraries(${ANA_LIB} ${Boost_LIBRARIES} ${LIB} ${COMPONENT_LIBS} ${Geant4_LIBRARIES} ${ROOT_LIBRARIES})

