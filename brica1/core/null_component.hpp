/******************************************************************************
**
** null_component.hpp
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

#ifndef __BRICA1_NULL_OMPONENT_HPP__
#define __BRICA1_NULL_OMPONENT_HPP__

#include "component.hpp"

namespace brica {
  class null_component : virtual public component {
  public:
    virtual void fire();
  };
}

#endif
