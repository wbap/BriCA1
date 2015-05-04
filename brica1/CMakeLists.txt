cmake_minimum_required(VERSION 2.8)
add_subdirectory(core)

################################
# Testing
################################
if (test)
  # This adds another subdirectory, which has 'project(gtest)'.
  add_subdirectory(lib/gtest-1.7.0)

  enable_testing()
endif()
