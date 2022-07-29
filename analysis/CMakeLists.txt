
#binary executables
#set(BIN AnaTaggerCounters RecoBPC AnaRPCounters AnaRPRecoCreate AnaRPRecoApply AnaSpect AnaSpectRecoCreate AnaSpectRecoApply)
set(BIN RecoBPC) # AnaRPRecoCreate AnaRPRecoApply AnaSpect AnaSpectRecoCreate AnaSpectRecoApply)

foreach(ibin ${BIN})
  add_executable(${ibin} src/${ibin}.cxx)
  target_link_libraries(${ibin} ${LIB} ${COMPONENT_LIBS} ${Boost_LIBRARIES} ${ROOT_LIBRARIES})
endforeach()

