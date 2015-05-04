set(CPP_FILES component.cpp module.cpp null_component.cpp port.cpp vector.cpp)

set(CMAKE_CXX_FLAGS "-g -Wall -std=c++11")

add_library(brica1-core SHARED ${CPP_FILES})

################################
# Testing
################################
if (test)
  # Include the gtest library. gtest_SOURCE_DIR is available due to
  # 'project(gtest)' above.
  #include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR} ${PROJECT_SOURCE_DIR})
  include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})

  ##############
  # Unit Tests
  ##############
  add_executable(runUnitTests ${CMAKE_CURRENT_SOURCE_DIR}/tests/brica1_unittest.cpp)

  # Standard linking to gtest stuff.
  target_link_libraries(runUnitTests gtest gtest_main brica1-core)

  # This is so you can do 'make test' to see all your tests run, instead of
  # manually running the executable runUnitTests to see those specific tests.
  add_test(NAME spira-test COMMAND runUnitTests)

  # You can also omit NAME and COMMAND. The second argument could be some other
  # test executable.
  #add_test(that-other-test-I-made runUnitTests)
endif()
