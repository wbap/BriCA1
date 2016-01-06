/******************************************************************************
 *
 * brica1/core/component.hpp
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

#ifndef __BRICA1_CORE_COMPONENT__
#define __BRICA1_CORE_COMPONENT__

#include <functional>
#include <map>
#include <memory>
#include <string>
#include <cassert>
#include "brica1/core/any.hpp"
#include "brica1/core/dictionary.hpp"
#include "brica1/core/port.hpp"
#include "brica1/core/unit.hpp"

namespace brica1 {
  namespace core {
    std::pair<Dictionary, Dictionary> fire_default(Dictionary, Dictionary);
    typedef std::function<std::pair<Dictionary, Dictionary>(Dictionary, Dictionary)> FireType;
    class Component : public Unit {
    public:
      Component(FireType f=fire_default);
      Component(const Component& other);
      Component(Component&& other) noexcept;
      Component& operator =(const Component& other);
      Component& operator =(Component&& other) noexcept;
      friend void swap(Component& a, Component& b);
      template<typename U>
      void make_in_port(std::string key);
      Port get_in_port(std::string key);
      void remove_in_port(std::string key);
      template<typename U>
      void make_out_port(std::string key);
      Port get_out_port(std::string key);
      void remove_out_port(std::string key);
      type::any get_input(std::string key);
      void set_input(std::string key, type::any value);
      template<typename U>
      void make_state(std::string key);
      type::any get_state(std::string key);
      void set_state(std::string key, type::any value);
      void remove_state(std::string key);
      type::any get_output(std::string key);
      void set_output(std::string key, type::any value);
      void input(double time);
      void output(double time);
      void fire();
      void reset();
    private:
      struct impl; std::shared_ptr<impl> pimpl;
    };
  }
}

#include "brica1/core/component_impl.hpp"

#endif
