/******************************************************************************
 *
 * brica1/core/dictionary_impl.hpp
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

namespace brica1 {
  namespace core {
    struct Dictionary::impl {
      std::map<std::string, type::any> map;
    };
    
    Dictionary::Dictionary() : pimpl(new impl()) {}
    
    Dictionary::Dictionary(const Dictionary& other) : pimpl(other.pimpl) {}
    
    Dictionary::Dictionary(Dictionary&& other) noexcept : pimpl(other.pimpl) {
      other.pimpl.reset();
    }
    
    Dictionary& Dictionary::operator =(const Dictionary& other) {
      Dictionary another(other);
      *this = std::move(another);
      return *this;
    }
    
    Dictionary& Dictionary::operator =(Dictionary&& other) noexcept {
      swap(*this, other);
      return *this;
    }
    
    void swap(Dictionary& a, Dictionary& b) {
      std::swap(a.pimpl, b.pimpl);
    }

    Dictionary Dictionary::clone() {
      Dictionary another;
      foreach([&](const std::string key, type::any& value){
          another[key] = value;
        });
      return another;
    }

    type::any& Dictionary::operator [](std::string key) {
      if(pimpl->map.find(key) == pimpl->map.end()) {
        pimpl->map.emplace(std::pair<std::string, type::any>(key, 0));
      }
      return pimpl->map.at(key);
    }

    void Dictionary::erase(std::string key) {
      if(pimpl->map.find(key) != pimpl->map.end()) {
        pimpl->map.erase(key);
      }
    }

    void Dictionary::foreach(std::function<void(const std::string, type::any&)> f) {
      std::map<std::string, type::any>::iterator iter;
      for(iter = pimpl->map.begin(); iter != pimpl->map.end(); ++iter) {
        f(iter->first, iter->second);
      }
    }
  }
}
