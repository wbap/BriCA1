/******************************************************************************
 *
 * tests/benchmark.cpp
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

#include "benchmark/benchmark.h"
#include "brica1/brica1.hpp"

#include <vector>

static void virtualtimesync_empty(benchmark::State& state) {
  brica1::core::Agent agent;
  brica1::schedulers::VirtualTimeSyncScheduler scheduler(agent);

  while(state.KeepRunning()) {
    scheduler.step();
  }
}

static void virtualtimesync_const_null(benchmark::State& state) {
  brica1::core::Component compA = brica1::components::Constant::create();
  brica1::core::Component compB = brica1::components::Null::create();
  brica1::core::Agent agent;

  agent.add_component("compA", compA);
  agent.add_component("compB", compB);

  brica1::schedulers::VirtualTimeSyncScheduler scheduler(agent);

  compA.make_out_port<std::vector<int> >("out");
  compB.make_in_port<std::vector<int> >("in");

  brica1::core::connect(compA, "out", compB, "in");

  compA.set_state("out", std::vector<int>(state.range_x()));

  while(state.KeepRunning()) {
    scheduler.step();
  }
}

BENCHMARK(virtualtimesync_empty);
BENCHMARK(virtualtimesync_const_null)->Arg(1)->Arg(28*28)->Arg(256*256*3);

BENCHMARK_MAIN();
