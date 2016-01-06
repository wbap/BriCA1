/******************************************************************************
 *
 * brica1/core/agent.hpp
 *
 * @author Copyright (C) 2016 Kotone Itaya
 * @version 1.0.0
 * @created  2016/01/06 Kotone Itaya -- Created!
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

#ifndef __BRICA1_CORE_AGENT__
#define __BRICA1_CORE_AGENT__

#include <list>
#include <map>
#include <memory>
#include "brica1/core/module.hpp"

namespace brica1 {
  namespace core {
    class Agent : public Module {
    public:
      Agent();
      Agent(const Agent& other);
      Agent(Agent&& other) noexcept;
      Agent& operator =(const Agent& other);
      Agent& operator =(Agent&& other) noexcept;
      friend void swap(Agent& a, Agent& b);
      void clone();
      std::list<Component> get_all_components();
      void reset();
    private:
      struct impl; std::shared_ptr<impl> pimpl;
    };
  }
}

#include "brica1/core/agent_impl.hpp"

#endif
