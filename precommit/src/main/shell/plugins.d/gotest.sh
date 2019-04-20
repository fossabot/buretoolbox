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

add_test_format gotest

GOTEST_FAILED_TESTS=""
GOTEST_LOG_DIR="target/go"

function gotest_parse_args
{
  declare i

  for i in "$@"; do
    case ${i} in
      --gotest-log-dir=*)
        delete_parameter "${i}"
        GOTEST_LOG_DIR=${i#=*}
      ;;
    esac
  done
}

function gotest_usage
{
  yetus_add_option "--gotest-log-dir=<dir>" "Directory relative to the module for go test output (default: \"${GOTEST_LOG_DIR}\")"
}

function gotest_process_tests
{
  # shellcheck disable=SC2034
  declare module=$1
  # shellcheck disable=SC2034
  declare buildlogfile=$2
  declare filefrag=$3
  declare result=0
  declare module_failed_tests
  declare filenames

  if [[ -d "${GOTEST_LOG_DIR}" ]]; then
    filenames=$(find "${GOTEST_LOG_DIR}" -type f -exec "${GREP}" -l -E "^\s*--- FAIL" {} \;)
  fi

  if [[ -n "${filenames}" ]]; then
    module_failed_tests=$(echo "${filenames}" \
      | "${SED}" -e "s,${GOTEST_LOG_DIR},,g" -e s,^/,,g )
    # shellcheck disable=SC2086
    cat ${filenames} >> "${PATCH_DIR}/patch-${filefrag}.gotest"
    GOTEST_LOGS="${GOTEST_LOGS} @@BASE@@/patch-${filefrag}.gotest"
    GOTEST_FAILED_TESTS="${GOTEST_FAILED_TESTS} ${module_failed_tests}"
    ((result=result+1))
  fi

  if [[ ${result} -gt 0 ]]; then
    return 1
  fi
  return 0
}

function gotest_finalize_results
{
  declare jdk=$1

  if [[ -n "${GOTEST_FAILED_TESTS}" ]] ; then
    # shellcheck disable=SC2086
    populate_test_table "${jdk}Failed GOTEST tests" ${GOTEST_FAILED_TESTS}
    GOTEST_FAILED_TESTS=""
    add_footer_table "GOTEST logs" "${GOTEST_LOGS}"
  fi
}
