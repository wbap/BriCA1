/******************************************************************************
 *
 * brica1/schedulers/virtualtimesyncscheduler.hpp
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

#ifndef __BRICA1_SCHEDULERS_VIRTUALTIMESYNCSCHEDULER__
#define __BRICA1_SCHEDULERS_VIRTUALTIMESYNCSCHEDULER__

#include <list>
#include <memory>
#include "brica1/core/component.hpp"
#include "brica1/core/scheduler.hpp"

namespace brica1 {
  namespace schedulers {
    class VirtualTimeSyncScheduler : public core::Scheduler {
    public:
      VirtualTimeSyncScheduler(core::Agent agent, double interval=1.0);
      VirtualTimeSyncScheduler(const VirtualTimeSyncScheduler& other);
      VirtualTimeSyncScheduler(VirtualTimeSyncScheduler&& other) noexcept;
      VirtualTimeSyncScheduler& operator =(const VirtualTimeSyncScheduler& other);
      VirtualTimeSyncScheduler& operator =(VirtualTimeSyncScheduler&& other) noexcept;
      friend void swap(VirtualTimeSyncScheduler& a, VirtualTimeSyncScheduler& b);
      void clone();
      inline double step();
    private:
      struct impl; std::shared_ptr<impl> pimpl;
    };
  }
}

#include "brica1/schedulers/virtualtimesyncscheduler_impl.hpp"

#endif
