/******************************************************************************
 *
 * brica1/core/unit_impl.hpp
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
    struct Unit::impl {
      std::map<std::string, Port> in_ports;
      std::map<std::string, Port> out_ports;
    };

    Unit::Unit() : pimpl(new impl()) {}

    Unit::Unit(const Unit& other) : pimpl(other.pimpl) {}

    Unit::Unit(Unit&& other) noexcept : pimpl(other.pimpl) {
      other.pimpl.reset();
    }

    Unit& Unit::operator =(const Unit& other) {
      Unit another(other);
      *this = std::move(another);
      return *this;
    }

    Unit& Unit::operator =(Unit&& other) noexcept {
      swap(*this, other);
      return *this;
    }

    void swap(Unit& a, Unit& b) {
      std::swap(a.pimpl, b.pimpl);
    }

    template<typename U>
    void Unit::make_in_port(std::string key) {
      pimpl->in_ports.emplace(std::pair<std::string, Port>(key, Port(U())));
    }

    Port Unit::get_in_port(std::string key) {
      return pimpl->in_ports.at(key);
    }

    void Unit::set_in_port(std::string key, Port port) {
      pimpl->in_ports.at(key) = port;
    }

    void Unit::remove_in_port(std::string key) {
      pimpl->in_ports.erase(key);
    }

    void Unit::alias_in_port(Unit& from_unit, std::string from_id, std::string to_id) {
      Port from = from_unit.get_in_port(from_id);
      set_in_port(to_id, from);
    }

    template<typename U>
    void Unit::make_out_port(std::string key) {
      pimpl->out_ports.emplace(std::pair<std::string, Port>(key, Port(U())));
    }

    void Unit::set_out_port(std::string key, Port port) {
      pimpl->out_ports.at(key) = port;
    }

    Port Unit::get_out_port(std::string key) {
      return pimpl->out_ports.at(key);
    }

    void Unit::remove_out_port(std::string key) {
      pimpl->out_ports.erase(key);
    }

    void Unit::alias_out_port(Unit& from_unit, std::string from_id, std::string to_id) {
      Port from = from_unit.get_out_port(from_id);
      set_out_port(to_id, from);
    }

    void Unit::connect(Unit from_unit, std::string from_id, std::string to_id) {
      Port from = from_unit.get_out_port(from_id);
      Port to = get_in_port(to_id);
      to.connect(from);
    }

    void connect(Unit from, std::string from_id, Unit to, std::string to_id) {
      to.connect(from, from_id, to_id);
    }
  }
}
