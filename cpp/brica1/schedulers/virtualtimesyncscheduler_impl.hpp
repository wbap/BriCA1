/******************************************************************************
 *
 * brica1/schedulers/virtualtimesyncscheduler_impl.hpp
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

#include <omp.h>
#include <unistd.h>
namespace brica1 {
  namespace schedulers {
    struct VirtualTimeSyncScheduler::impl {
      double time=0.0;
      double interval;
    };
    
    VirtualTimeSyncScheduler::VirtualTimeSyncScheduler(core::Agent agent, double interval) : Scheduler(agent), pimpl(new impl()) {
      pimpl->interval = interval;
    }
    
    VirtualTimeSyncScheduler::VirtualTimeSyncScheduler(const VirtualTimeSyncScheduler& other) : pimpl(other.pimpl) {}
    
    VirtualTimeSyncScheduler::VirtualTimeSyncScheduler(VirtualTimeSyncScheduler&& other) noexcept : pimpl(other.pimpl) {
      other.pimpl = nullptr;
    }
    
    VirtualTimeSyncScheduler& VirtualTimeSyncScheduler::operator =(const VirtualTimeSyncScheduler& other) {
      VirtualTimeSyncScheduler another(other);
      *this = std::move(another);
      return *this;
    }
    
    VirtualTimeSyncScheduler& VirtualTimeSyncScheduler::operator =(VirtualTimeSyncScheduler&& other) noexcept {
      swap(*this, other);
      return *this;
    }
    
    void swap(VirtualTimeSyncScheduler& a, VirtualTimeSyncScheduler& b) {
      std::swap(a.pimpl, b.pimpl);
    }
    
    void VirtualTimeSyncScheduler::clone() {
      
    }

    double VirtualTimeSyncScheduler::step() {
      std::vector<core::Component> components = get_components();
      std::vector<core::Component>::iterator component;

      const auto num_components = components.size();

#pragma omp parallel
      {

#pragma omp for 
          for(size_t i = 0; i < num_components; ++i) {
              components[i].input(pimpl->time);
          }

#pragma omp for
          for(size_t i = 0; i < num_components; ++i) {
              components[i].fire();
          }

#pragma omp single
          {
              time() += pimpl->interval;
          }

#pragma omp for
          for(size_t i = 0; i < num_components; ++i) {
              components[i].output(pimpl->time);
          }
      }


      return time();
    }
  }
}
