/******************************************************************************
 *
 * brica1/core/agent_impl.hpp
 *
 * @author Copyright (C) 2016 Kotone Itaya
 * @version 1.0.0
 * @created  2016/01/06 Kotone Itaya -- Created!
 * @@
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 *****************************************************************************/

namespace brica1 {
  namespace core {
    struct Agent::impl {

    };
    
    Agent::Agent() : pimpl(new impl()) {}
    
    Agent::Agent(const Agent& other) : Module(other), pimpl(other.pimpl) {}
    
    Agent::Agent(Agent&& other) noexcept : Module(other), pimpl(other.pimpl) {
      other.pimpl.reset();
    }
    
    Agent& Agent::operator =(const Agent& other) {
      Agent another(other);
      *this = std::move(another);
      return *this;
    }
    
    Agent& Agent::operator =(Agent&& other) noexcept {
      swap(dynamic_cast<Module&>(*this), dynamic_cast<Module&>(other));
      swap(*this, other);
      return *this;
    }
    
    void swap(Agent& a, Agent& b) {
      std::swap(a.pimpl, b.pimpl);
    }
    
    void Agent::clone() {
      
    }

    std::vector<Component> get_all_components_recursive(Module module) {
      std::vector<Component> components = module.get_components();
      std::vector<Module> submodules = module.get_submodules();
      std::vector<Module>::iterator submodule;
      for(submodule = submodules.begin(); submodule != submodules.end(); ++submodule) {
        std::vector<Component> tmp = get_all_components_recursive(*submodule);
        std::vector<Component>::iterator component;
        for(component = tmp.begin(); component != tmp.end(); ++component) {
          components.push_back(*component);
        }
      }
      return components;
    }

    std::vector<Component> Agent::get_all_components() {
      return get_all_components_recursive(*this);
    }

    void Agent::reset() {
      std::vector<Component> components = get_all_components();
      std::vector<Component>::iterator component;
      for(component = components.begin(); component != components.end(); ++component) {
        component->reset();
      }
    }
  }
}
