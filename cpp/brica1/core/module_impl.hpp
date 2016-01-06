/******************************************************************************
 *
 * brica1/core/module_impl.hpp
 *
 * @author Copyright (C) 2015 Kotone Itaya
 * @version 1.0.0
 * @created  2015/11/30 Kotone Itaya -- Created!
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
    struct Module::impl {
      std::map<std::string, Component> components;
      std::map<std::string, Module> submodules;
    };
    
    Module::Module() : pimpl(new impl()) {}
    
    Module::Module(const Module& other) : Unit(other), pimpl(other.pimpl) {}
    
    Module::Module(Module&& other) noexcept : Unit(other), pimpl(other.pimpl) {
      other.pimpl.reset();
    }
    
    Module& Module::operator =(const Module& other) {
      Module another(other);
      *this = std::move(another);
      return *this;
    }
    
    Module& Module::operator =(Module&& other) noexcept {
      swap(dynamic_cast<Unit&>(*this), dynamic_cast<Unit&>(other));
      swap(*this, other);
      return *this;
    }
    
    void swap(Module& a, Module& b) {
      std::swap(a.pimpl, b.pimpl);
    }

    void Module::add_component(std::string key, Component component) {
      pimpl->components[key] = component;
    }

    Component Module::get_component(std::string key) {
      return pimpl->components[key];
    }

    std::list<Component> Module::get_components() {
      std::map<std::string, Component>::iterator iter;
      std::list<Component> components;
      for(iter = pimpl->components.begin(); iter != pimpl->components.end(); ++iter) {
        Component component = iter->second;
        components.push_back(component);
      }
      return components;
    }

    void Module::remove_component(std::string key) {
      pimpl->components.erase(key);
    }

    void Module::add_submodule(std::string key, Module module) {
      pimpl->submodules[key] = module;
    }

    Module Module::get_submodule(std::string key) {
      return pimpl->submodules[key];
    }

    std::list<Module> Module::get_submodules() {
      std::map<std::string, Module>::iterator iter;
      std::list<Module> submodules;
      for(iter = pimpl->submodules.begin(); iter != pimpl->submodules.end(); ++iter) {
        Module submodule = iter->second;
        submodules.push_back(submodule);
      }
      return submodules;
    }

    void Module::remove_submodule(std::string key) {
      pimpl->submodules.erase(key);
    }
  }
}
