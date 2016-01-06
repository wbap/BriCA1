/******************************************************************************
 *
 * brica1/core/dictionary.hpp
 *
 * @author Copyright (C) 2015 Kotone Itaya
 * @version 1.0.0
 * @created  2015/11/27 Kotone Itaya -- Created!
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

#ifndef __BRICA1_CORE_DICTIONARY__
#define __BRICA1_CORE_DICTIONARY__

#include <map>
#include <memory>
#include <functional>
#include "brica1/core/any.hpp"

namespace brica1 {
  namespace core {
    class Dictionary {
    public:
      Dictionary();
      Dictionary(const Dictionary& other);
      Dictionary(Dictionary&& other) noexcept;
      Dictionary& operator =(const Dictionary& other);
      Dictionary& operator =(Dictionary&& other) noexcept;
      friend void swap(Dictionary& a, Dictionary& b);
      Dictionary clone();
      type::any& operator [](std::string key);
      void erase(std::string key);
      void foreach(std::function<void(const std::string, type::any&)> f);
    private:
      struct impl; std::shared_ptr<impl> pimpl;
    };
  }
}

#include "brica1/core/dictionary_impl.hpp"

#endif
