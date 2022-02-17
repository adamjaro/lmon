
#local library
set(RP_LIB lmonRP)

#local include
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

#sources and headers for local library
file(GLOB det_src ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cxx)
file(GLOB det_inc ${CMAKE_CURRENT_SOURCE_DIR}/include/*.h)

#build the local library
add_library (${RP_LIB} SHARED ${det_src} ${det_inc})
target_link_libraries(${RP_LIB} ${Geant4_LIBRARIES} ${ROOT_DEPS})

#add for top cmake
set(COMPONENT_LIBS ${COMPONENT_LIBS} ${RP_LIB} PARENT_SCOPE)
set(COMPONENT_INCLUDE ${COMPONENT_INCLUDE} ${CMAKE_CURRENT_SOURCE_DIR}/include PARENT_SCOPE)

