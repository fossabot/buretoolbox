#!/usr/bin/env bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# no public APIs here
# SHELLDOC-IGNORE

# shellcheck disable=2034
if [[ "${DRONE}" = true ]] && [[ -n "${DRONE_SYSTEM_VERSION}" ]] &&
  declare -f compile_cycle >/dev/null; then

  ROBOT=true
  ROBOTTYPE=drone
  BUILDMODE=full
  BUILD_URL=${DRONE_BUILD_LINK}/${DRONE_STAGE_NUMBER}/${DRONE_STEP_NUMBER}
  BUILD_URL_CONSOLE=''

  if [[ -e ${DRONE_WORKSPACE_BASE}/.git ]]; then
    BASEDIR=${DRONE_WORKSPACE_BASE}
    pushd "${BASEDIR}" >/dev/null || exit 1
    echo "Attempting to reset Drone's understanding of ${DRONE_BRANCH}"
    "${GIT}" branch --set-upstream-to=origin/"${DRONE_BRANCH}" "${DRONE_BRANCH}" || true
    "${GIT}" branch -f  "${DRONE_BRANCH}" origin/"${DRONE_BRANCH}" || true
    popd >/dev/null || exit 1
  fi

  if [[ -n "${DRONE_PULL_REQUEST}" ]]; then
    if [[ -n "${DRONE_GITLAB_SERVER}" ]]; then
      PATCH_OR_ISSUE="GL:${DRONE_PULL_REQUEST}"
    else
      PATCH_OR_ISSUE="GH:${DRONE_PULL_REQUEST}"
    fi

    if [[ -n "${PATCH_OR_ISSUE}" ]]; then
      USER_PARAMS+=("${PATCH_OR_ISSUE}")
    fi

  else
    PATCH_BRANCH="${DRONE_BRANCH}"
    BUILDMODE=full
    USER_PARAMS+=("--empty-patch")
  fi

  yetus_add_array_element EXEC_MODES Drone
  yetus_add_array_element EXEC_MODES ResetRepo
  yetus_add_array_element EXEC_MODES Robot
  yetus_add_array_element EXEC_MODES UnitTests

  add_docker_env \
    DRONE \
    DRONE_BRANCH \
    DRONE_BUILD_LINK \
    DRONE_PULL_REQUEST \
    DRONE_REPO_LINK \
    DRONE_STAGE_NUMBER \
    DRONE_STEP_NUMBER \
    DRONE_SYSTEM_VERSION \
    DRONE_WORKSPACE_BASE
fi

function drone_set_plugin_defaults
{
  if [[ ${DRONE_REPO_LINK} =~ github.com ]]; then
    if declare -f  github_breakup_url >/dev/null 2>&1; then
      github_breakup_url "${DRONE_REPO_LINK}"
    fi
    GITHUB_REPO=${DRONE_REPO_OWNER}/${DRONE_REPO_NAME}
  elif [[ -n "${DRONE_GITLAB_SERVER}" ]]; then
    if declare -f  gitlab_breakup_url >/dev/null 2>&1; then
      gitlab_breakup_url "${DRONE_REPO_LINK}"
    fi
    GITLAB_REPO=${DRONE_REPO_OWNER}/${DRONE_REPO_NAME}
  fi
}

function drone_finalreport
{
  add_footer_table "Console output" "${BUILD_URL}"
}
