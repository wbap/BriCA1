/******************************************************************************
 *
 * brica1/core/component_impl.hpp
 *
 * @author Copyright (C) 2015 Kotone Itaya
 * @version 1.0.0
 * @created  2015/11/26 Kotone Itaya -- Created!
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
    std::pair<Dictionary, Dictionary> fire_default(Dictionary inputs, Dictionary states) {
      Dictionary outputs;
      return std::pair<Dictionary, Dictionary>(outputs, states);
    }

    struct Component::impl {
      impl(
           FireType f,
           double init_offset=0.0,
           double init_interval=1.0
           ) :
        offset(init_offset),
        interval(init_interval),
        fire(f)
      {}
      double last_input_time=0.0;
      double last_output_time=0.0;
      double offset;
      double interval;
      Dictionary inputs;
      Dictionary states;
      Dictionary outputs;
      FireType fire;
    };
    
    Component::Component(FireType f) : pimpl(new impl(f)) {}

    Component::Component(const Component& other) : Unit(other), pimpl(other.pimpl) {}

    Component::Component(Component&& other) noexcept : Unit(other), pimpl(other.pimpl) {
      other.pimpl.reset();
    }
    
    Component& Component::operator =(const Component& other) {
      Component another(other);
      *this = std::move(another);
      return *this;
    }
    
    Component& Component::operator =(Component&& other) noexcept {
      swap(dynamic_cast<Unit&>(*this), dynamic_cast<Unit&>(other));
      swap(*this, other);
      return *this;
    }
    
    void swap(Component& a, Component& b) {
      std::swap(a.pimpl, b.pimpl);
    }

    template<typename U>
    void Component::make_in_port(std::string key) {
      Unit::make_in_port<U>(key);
      pimpl->inputs[key] = 0;
    }

    Port Component::get_in_port(std::string key) {
      return Unit::get_in_port(key);
    }

    void Component::remove_in_port(std::string key) {
      Unit::remove_in_port(key);
      pimpl->inputs.erase(key);
    }

    template<typename U>
    void Component::make_out_port(std::string key) {
      Unit::make_out_port<U>(key);
      pimpl->outputs[key] = 0;
    }

    Port Component::get_out_port(std::string key) {
      return Unit::get_out_port(key);
    }

    void Component::remove_out_port(std::string key) {
      Unit::remove_out_port(key);
      pimpl->outputs.erase(key);
    }

    type::any Component::get_input(std::string key) {
      return pimpl->inputs[key];
    }

    void Component::set_input(std::string key, type::any value) {
      pimpl->inputs[key] = value;
    }

    template<typename U>
    void Component::make_state(std::string key) {
      pimpl->states[key] = U();
    }

    type::any Component::get_state(std::string key) {
      return pimpl->states[key];
    }

    void Component::set_state(std::string key, type::any value) {
      pimpl->states[key] = value;
    }

    void Component::remove_state(std::string key) {
      pimpl->states.erase(key);
    }

    void Component::set_output(std::string key, type::any value) {
      pimpl->outputs[key] = value;
    }

    type::any Component::get_output(std::string key) {
      return pimpl->outputs[key];
    }

    void Component::input(double time) {
      assert(pimpl->last_input_time <= time);
      pimpl->last_input_time = time;
      pimpl->inputs.foreach([&](const std::string key, type::any& value){
          Port port = get_in_port(key);
          port.sync();
          value = port.get_buffer();
        });
    }

    void Component::output(double time) {
      assert(pimpl->last_output_time <= time);
      pimpl->last_output_time = time;
      pimpl->outputs.foreach([&](const std::string key, type::any& value){
          Port port = get_out_port(key);
          port.set_buffer(value);
        });
    }

    void Component::fire() {
      std::pair<Dictionary, Dictionary> results = pimpl->fire(pimpl->inputs, pimpl->states);
      pimpl->outputs = results.first;
      pimpl->states = results.second;
    }

    void Component::reset() {
      pimpl->last_input_time = 0.0;
      pimpl->last_output_time = 0.0;
    }
  }
}
