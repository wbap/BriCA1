/******************************************************************************
 *
 * brica1/core/components/constant_impl.hpp
 *
 * @author Copyright (C) 2016 Kotone Itaya
 * @version 1.0.0
 * @created  2016/01/01 Kotone Itaya -- Created!
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
  namespace components {
    namespace Constant {
      std::pair<core::Dictionary, core::Dictionary> fire(core::Dictionary inputs, core::Dictionary states) {
        core::Dictionary outputs;
        states.foreach([&](const std::string key, type::any& value){
            outputs[key] = value;
          });
        return std::pair<core::Dictionary, core::Dictionary>(outputs, states);
      }

      core::Component create() {
        core::Component component(fire);
        return component;
      }
    }
  }
}
