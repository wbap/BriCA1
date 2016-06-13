cmake_minimum_required(VERSION 2.8)

option(test "Build all tests." OFF)
option(benchmark "Build all benchmarks." OFF)

set(PROJECT_NAME BriCA1)
project(${PROJECT_NAME})
set(BRICA1_VERSION_MAJOR 1)
set(BRICA1_VERSION_MINOR 0)
set(BRICA1_VERSION_PATCH 0)

set(CMAKE_CXX_FLAGS "-g -Wall -O2 -fopenmp")

# If you want your own include/ directory, set this, and then you can do
# include_directories(${COMMON_INCLUDES}) in other CMakeLists.txt files.
include_directories(.)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

################################
# Normal Libraries & Executables
################################
# Nothing yet

################################
# Benchmarking
################################

if (benchmark)
  add_subdirectory(lib/benchmark-master)

  include_directories(${benchmark_SOURCE_DIR}/include ${benchmark_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/include)

  ##############
  # Benchmarks
  ##############

  add_executable(runBenchmarks tests/benchmark.cpp)

  target_link_libraries(runBenchmarks benchmark)
endif()

################################
# Testing
################################
if (test)
  # This adds another subdirectory, which has 'project(gtest)'.
  add_subdirectory(lib/gtest-1.7.0)

  enable_testing()

  # Include the gtest library. gtest_SOURCE_DIR is available due to
  # 'project(gtest)' above.
  include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/include)

  ##############
  # Unit Tests
  ##############
  #add_executable(runUnitTests tests/virtual.cpp)

  # Standard linking to gtest stuff.
  #target_link_libraries(runUnitTests gtest gtest_main)

  # This is so you can do 'make test' to see all your tests run, instead of
  # manually running the executable runUnitTests to see those specific tests.
  #add_test(NAME spira-test COMMAND runUnitTests)

  # You can also omit NAME and COMMAND. The second argument could be some other
  # test executable.
  #add_test(that-other-test-I-made runUnitTests)
endif()

install(
  DIRECTORY "${PROJECT_SOURCE_DIR}/include/brica1"
  DESTINATION include
  FILES_MATCHING PATTERN "*.*hpp")
