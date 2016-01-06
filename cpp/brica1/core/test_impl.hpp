/******************************************************************************
 *
 * brica1/core/test_impl.hpp
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
    struct Test::impl {
      
    };
    
    Test::Test() : pimpl(new impl()) {}
    
    Test::Test(const Test& other) : pimpl(other.pimpl) {}
    
    Test::Test(Test&& other) noexcept : pimpl(other.pimpl) {
      other.pimpl = nullptr
    }
    
    Test& Test::operator =(const Test& other) {
      const Test another(other)
      *this = std::move(another);
      return *this;
    }
    
    Test& Test::operator =(Test&& other) noexcept {
      swap(*this, other)
      return *this;
    }
    
    void Test::swap(Test& a, Test& b) {
      std::swap(a.pimpl, b.pimpl)
    }
  }
}
