/******************************************************************************
 *
 * brica1/core/port_impl.hpp
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
    struct Port::impl {
      impl() : buffer(0) {}
      type::any buffer;
      std::weak_ptr<impl> target;
    };

    Port::Port() : pimpl(new impl()) {}

    template<typename U>
    Port::Port(U buffer) : pimpl(new impl()) {
      pimpl->buffer = buffer;
    }

    Port::Port(const Port& other) : pimpl(other.pimpl) {}

    Port::Port(Port&& other) noexcept : pimpl(other.pimpl) {
      other.pimpl.reset();
    }

    Port& Port::operator =(const Port& other) {
      Port another(other);
      *this = std::move(another);
      return *this;
    }

    Port& Port::operator =(Port&& other) noexcept {
      swap(*this, other);
      return *this;
    }

    Port Port::clone() {
      Port another;
      another.pimpl->buffer = pimpl->buffer;
      another.pimpl->target = pimpl->target;
      return another;
    }

    void swap(Port& a, Port& b) {
      std::swap(a.pimpl, b.pimpl);
    }

    type::any Port::get_buffer() {
      return pimpl->buffer;
    }

    void Port::set_buffer(type::any value) {
      pimpl->buffer = value;
    }
    void Port::connect(Port target) {
      pimpl->target = target.pimpl;
    }

    void Port::sync() {
      if(std::shared_ptr<impl> target = pimpl->target.lock()) {
        pimpl->buffer = target->buffer;
      }
    }
  }
}

