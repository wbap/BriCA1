/******************************************************************************
**
** component.hpp
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

#ifndef __BRICA1_COMPONENT_HPP__
#define __BRICA1_COMPONENT_HPP__

#include <string>
#include <map>

#include "connection.hpp"
#include "port.hpp"
#include "types.hpp"
#include "vector.hpp"

namespace brica {
  class component {
  public:
    component();
    virtual void fire()=0;

    void makeInPort(std::string id, int32 length);
    void removeInPort(std::string id);
    vector getInPort(std::string id);
    void makeOutPort(std::string id, int32 length);
    void removeOutPort(std::string id);
    vector getOutPort(std::string id);
    void setState(std::string id, vector v);
    vector getState(std::string id);
    void clearState();
    void setResult(std::string id, vector v);
    vector getResult(std::string id);
    void clearResult();
    class port;

  protected:
    float64 lastInputTime;
    float64 lastOutputTime;
    float64 interval;

    // Input/output ports of this module.
    // in ports and out ports are updated automatically.
    // Users instead should work on states and results below.
    std::map<std::string, vector> in_ports;
    std::map<std::string, vector>& out_ports;

    std::map<std::string, vector> states;
    std::map<std::string, vector>& results;

    // Double output buffers.
    // These buffers are used internally by this class to hide calculation.
    std::map<std::string, vector> buffer0;
    std::map<std::string, vector> buffer1;

    std::vector<connection> connections;
  };
}

#endif
