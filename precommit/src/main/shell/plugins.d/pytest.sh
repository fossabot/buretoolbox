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

# SHELLDOC-IGNORE

add_test_type pytest

PYTEST_TIMER=0

PYTEST=${PYTEST:-$(command -v pytest 2>/dev/null)}

function pytest_usage
{
  yetus_add_option "--pytest=<file>" "Filename of the pytest executable (default: ${PYTEST})"
  yetus_add_option "--pytest-config=<file>" "pytest configuration file"
}

function pytest_parse_args
{
  local i

  for i in "$@"; do
    case ${i} in
    --pytest=*)
      delete_parameter "${i}"
      PYTEST=${i#*=}
    ;;
    --pytest-config=*)
      delete_parameter "${i}"
      PYTEST_CONFIG_FILE=${i#*=}
    ;;
    esac
  done
}

function pytest_filefilter
{
  local filename=$1

  if [[ ${filename} =~ \.py$ ]]; then
    add_test pytest
  fi
}

function pytest_precheck
{
  if ! verify_command "pytest" "${PYTEST}"; then
    add_vote_table_v2 0 pytest "" "pytest was not available."
    delete_test pytest
  fi
}

function pytest_executor
{
  declare repostatus=$1
  declare i
  declare -a pytestopts

  if ! verify_needed_test pytest; then
    return 0
  fi

  big_console_header "pytest: ${BUILDMODE}"

  start_clock

  # add our previous elapsed to our new timer
  # by setting the clock back
  offset_clock "${PYTEST_TIMER}"

  pytestopts=()

  if [[ -n "${PYTEST_CONFIG_FILE}" ]] && [[ -f "${PYTEST_CONFIG_FILE}" ]]; then
    pytestopts+=('-c' "${PYTEST_CONFIG_FILE}")
  fi

  mkdir -p "${PATCH_DIR}/pytest"
  pytestopts+=("--junitxml=${PATCH_DIR}/pytest")

  echo "Running pytest against identified python scripts."
  pushd "${BASEDIR}" >/dev/null || return 1
  for i in "${CHANGED_FILES[@]}"; do
    if [[ ${i} =~ \.py$ && -f ${i} ]]; then
      "${PYTEST}" "${pytestopts[@]}" "${i}"
    fi
  done

  return 0
}

function pytest_postapply
{
  if ! verify_needed_test pytest; then
    return 0
  fi

  pytest_executor patch

  # shellcheck disable=SC2016
  PYTEST_VERSION=$("${PYTEST}" --version 2>/dev/null | "${GREP}" pytest | "${AWK}" '{print $NF}')
  add_version_data pytest "${PYTEST_VERSION%,}"


  root_postlog_compare \
    pytest \
    "${PATCH_DIR}/branch-pytest-result.txt" \
    "${PATCH_DIR}/patch-pytest-result.txt"
}

function pytest_postcompile
{
  declare repostatus=$1

  if [[ "${repostatus}" = branch ]]; then
    pytest_preapply
  else
    pytest_postapply
  fi
}
