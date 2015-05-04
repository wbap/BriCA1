/******************************************************************************
**
** component.cpp
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

#include <cassert>

#include "component.hpp"

namespace brica {
  component::component() : out_ports(buffer0), results(buffer1) {
    lastInputTime = 0.0;
    lastOutputTime = 0.0;
    interval = 1.0;
  }

  void component::makeInPort(std::string id, int32 length) {
    in_ports.insert(std::pair<std::string, vector>(id, zeros(length)));
  }

  void component::removeInPort(std::string id) {
    std::map<std::string, vector>::iterator iter = in_ports.find(id);
    if(iter != in_ports.end()) {
      in_ports.erase(iter);
    }
  }

  vector component::getInPort(std::string id) {
    std::map<std::string, vector>::iterator iter = in_ports.find(id);
    assert(iter != in_ports.end()); // The element must exist
    return iter->second;
  }

  void component::makeOutPort(std::string id, int32 length) {
    buffer0.insert(std::pair<std::string, vector>(id, zeros(length)));
    buffer1.insert(std::pair<std::string, vector>(id, zeros(length)));
  }

  void component::removeOutPort(std::string id) {
    std::map<std::string, vector>::iterator iter0 = buffer0.find(id);
    std::map<std::string, vector>::iterator iter1 = buffer1.find(id);
    if(iter0 != buffer0.end()) {
      buffer0.erase(iter0);
    }
    if(iter1 != buffer1.end()) {
      buffer1.erase(iter1);
    }
  }

  vector component::getOutPort(std::string id) {
    std::map<std::string, vector>::iterator iter = out_ports.find(id);
    assert(iter != out_ports.end()); // The element must exist
    return iter->second;
  }

  void component::setState(std::string id, vector v) {
    states.insert(std::pair<std::string, vector>(id, v));
  }

  vector component::getState(std::string id) {
    std::map<std::string, vector>::iterator iter = states.find(id);
    assert(iter != states.end());
    return iter->second;
  }

  void component::clearState() {
    states.clear();
  }

  void component::setResult(std::string id, vector v) {
    results.insert(std::pair<std::string, vector>(id, v));
  }

  vector component::getResult(std::string id) {
    std::map<std::string, vector>::iterator iter = results.find(id);
    assert(iter != results.end());
    return iter->second;
  }

  void component::clearResult() {
    results.clear();
  }

  class component::port {
  public:
    port(vector v);
  private:
    vector &buffer;
  };

  component::port::port(vector v) : buffer(v) { }
}
