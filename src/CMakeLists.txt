FILE(GLOB_RECURSE srcs ${CMAKE_SOURCE_DIR}/src/*.*)
idf_component_register(SRCS ${srcs})
