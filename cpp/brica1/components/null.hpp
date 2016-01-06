/******************************************************************************
 *
 * brica1/core/components/null.hpp
 *
 * @author Copyright (C) 2015 Kotone Itaya
 * @version 1.0.0
 * @created  2015/12/11 Kotone Itaya -- Created!
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

#ifndef __BRICA1_CORE_COMPONENTS_NULL__
#define __BRICA1_CORE_COMPONENTS_NULL__

#include <memory>
#include "brica1/core/component.hpp"

namespace brica1 {
  namespace components {
    namespace Null {
      std::pair<core::Dictionary, core::Dictionary> fire(core::Dictionary inputs, core::Dictionary states);

      core::Component create();
    }
  }
}

#include "brica1/components/null_impl.hpp"

#endif
