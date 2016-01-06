/******************************************************************************
 *
 * brica1/core/scheduler.hpp
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

#ifndef __BRICA1_CORE_SCHEDULER__
#define __BRICA1_CORE_SCHEDULER__

#include <list>
#include <memory>
#include "brica1/core/agent.hpp"

namespace brica1 {
  namespace core {
    class Scheduler {
    public:
      Scheduler();
      Scheduler(Agent agent);
      Agent get_agent();
      void set_agent(Agent agent);
      std::list<Component> get_components();
      void reset();
      virtual double step()=0;
    protected:
      double& time();
    private:
      struct impl; std::shared_ptr<impl> pimpl;
    };
  }
}

#include "brica1/core/scheduler_impl.hpp"

#endif
