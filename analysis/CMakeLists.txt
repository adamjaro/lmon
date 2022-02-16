
#binary executables
set(BIN AnaTaggerCounters RecoBPC AnaRPCounters)

foreach(ibin ${BIN})
  add_executable(${ibin} src/${ibin}.cxx)
  target_link_libraries(${ibin} ${LIB} ${COMPONENT_LIBS} ${Boost_LIBRARIES} ${ROOT_LIBRARIES})
endforeach()

