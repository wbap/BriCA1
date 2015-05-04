/******************************************************************************
**
** vector.cpp
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

#include "vector.hpp"

namespace brica {
  std::function<vector(int32)> vector_initializer(int16 value) {
    return std::function<vector(int32)>([=](int32 length){
      vector vec(length);
      for(vector::iterator iter = vec.begin(); iter != vec.end(); ++iter) {
        (*iter) = value;
      }
      return vec;
    });
  }

  vector zeros(int32 length) {
    return vector_initializer(0)(length);
  }

  vector ones(int32 length) {
    return vector_initializer(1)(length);
  }
}
