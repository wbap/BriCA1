/******************************************************************************
**
** brica1_unittest.cpp
** BriCA v1.0.0
**
** Copyright 2015 Kotone Itaya
**
** Licensed under the Apache License, Version 2.0 (the "License");
** you may not use this file except in compliance with the License.
** You may obtain a copy of the License at
**
**     http://www.apache.org/licenses/LICENSE-2.0
**
** Unless required by applicable law or agreed to in writing, software
** distributed under the License is distributed on an "AS IS" BASIS,
** WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
** See the License for the specific language governing permissions and
** limitations under the License.
**
******************************************************************************/


#include "gtest/gtest.h"
#include "core.hpp"

namespace brica {
  TEST(component, null) {
    null_component A;
    A.makeInPort("in0", 3);
    EXPECT_EQ(A.getInPort("in0"), zeros(3));
    A.makeOutPort("out0", 3);
    EXPECT_EQ(A.getOutPort("out0"), zeros(3));
1    A.setState("state0", zeros(3));
    EXPECT_EQ(A.getState("state0"), zeros(3));
    A.setResult("result0", zeros(3));
    EXPECT_EQ(A.getResult("result0"), zeros(3));
  }
}
