<!---
  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing,
  software distributed under the License is distributed on an
  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  KIND, either express or implied.  See the License for the
  specific language governing permissions and limitations
  under the License.
-->

# Robots: Drone

TRIGGER: ${DRONE}=true and ${DRONE_SYSTEM_VERSION} not empty

Drone lacks built-in support for artifacts.  Therefore setting `--patch-dir` and other settings will be required for generated log data to not be lost.  Similar to other CI systems, Apache Yetus will reset the appropriate git references in the cloned repository.

See also:

* Apache Yetus' source tree [.drone.yml](https://github.com/apache/yetus/blob/master/.drone.yaml) for some tips and tricks.
