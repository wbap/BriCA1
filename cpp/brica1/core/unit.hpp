/******************************************************************************
 *
 * brica1/core/unit.hpp
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

#ifndef __BRICA1_CORE_UNIT__
#define __BRICA1_CORE_UNIT__

#include <map>
#include <memory>
#include <string>
#include "brica1/core/port.hpp"

namespace brica1 {
  namespace core {
    class Unit {
    public:
      Unit();
      Unit(const Unit& other);
      Unit(Unit&& other) noexcept;
      Unit& operator =(const Unit& other);
      Unit& operator =(Unit&& other) noexcept;
      friend void swap(Unit& a, Unit& b);
      template<typename U>
      void make_in_port(std::string key);
      Port get_in_port(std::string key);
      void set_in_port(std::string key, Port port);
      void remove_in_port(std::string key);
      void alias_in_port(Unit& from_unit, std::string from_id, std::string to_id);
      template<typename U>
      void make_out_port(std::string key);
      Port get_out_port(std::string key);
      void set_out_port(std::string key, Port port);
      void remove_out_port(std::string key);
      void alias_out_port(Unit& from_unit, std::string from_id, std::string to_id);
      void connect(Unit from_unit, std::string from_id, std::string to_id);
    private:
      struct impl; std::shared_ptr<impl> pimpl;
    };

    void connect(Unit from, std::string from_id, Unit to, std::string to_id);
  }
}

#include "brica1/core/unit_impl.hpp"

#endif
