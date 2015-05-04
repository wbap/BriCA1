/******************************************************************************
**
** types.hpp
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

#ifndef __BRICA1_TYPES_HPP__
#define __BRICA1_TYPES_HPP__

#include <cstdint>
#include <vector>

namespace brica {
  typedef int8_t  int8;
  typedef int16_t int16;
  typedef int32_t int32;
  typedef int64_t int64;
  typedef uint8_t  uint8;
  typedef uint16_t uint16;
  typedef uint32_t uint32;
  typedef uint64_t uint64;

  typedef float float32;
  typedef double float64;

  typedef std::vector<int16> vector;
}

#endif
