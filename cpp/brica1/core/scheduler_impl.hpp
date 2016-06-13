/******************************************************************************
 *
 * brica1/core/scheduler_impl.hpp
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

namespace brica1 {
  namespace core {
    struct Scheduler::impl {
      Agent agent;
      std::vector<Component> components;
      double time=0.0;
    };
    
    Scheduler::Scheduler() : pimpl(new impl()) {}

    Scheduler::Scheduler(Agent agent) : pimpl(new impl()) {
      set_agent(agent);
    }
    
    Agent Scheduler::get_agent() {
      return pimpl->agent;
    }

    void Scheduler::set_agent(Agent agent) {
      reset();
      pimpl->agent = agent;
      pimpl->components = pimpl->agent.get_all_components();
    }

    std::vector<Component> Scheduler::get_components() {
      return pimpl->components;
    }

    void Scheduler::reset() {
      pimpl->components.clear();
      pimpl->agent.reset();
      pimpl->agent = Agent();
    }

    double& Scheduler::time() {
      return pimpl->time;
    }
  }
}
