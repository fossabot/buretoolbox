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


#shellcheck source=SCRIPTDIR/../precommit/src/main/shell/core.d/00-yetuslib.sh
. precommit/src/main/shell/core.d/00-yetuslib.sh


ORIGDIR=$(pwd)
VERSION=${1-0.14.0-RC1}
NONRC=${VERSION/-RC?/}
TMPDIR=/tmp/$$

cleanup() {

  cd "${ORIGDIR}"  || exit 1
  rm -rf "${TMPDIR}"
  exit 1
}

echo "Attempting to verify ${VERSION}"

mkdir -p "${TMPDIR}"

trap cleanup INT QUIT TRAP ABRT BUS SEGV TERM ERR

cd "${TMPDIR}" || exit 1
wget --recursive --no-parent \
  --quiet "https://dist.apache.org/repos/dist/dev/yetus/${VERSION}/"

curl --output KEYS.yetus --silent 'https://downloads.apache.org/yetus/KEYS'
gpg --import KEYS.yetus

cd "dist.apache.org/repos/dist/dev/yetus/${VERSION}/" || exit 1

readarray -d '' FILELIST < <(find . -type f -print0)

# remnant from wget
yetus_del_array_element FILELIST "./index.html"

for ascname in *.asc; do
  filename=${ascname/.asc/}
  echo "Testing ${filename}"
  if gpg --verify "${ascname}" "${filename}"; then
      yetus_del_array_element FILELIST "./${ascname}"
  fi

  sha512sum --tag  "${filename}" > "${filename}.my512"
  if diff "${filename}.sha512" "${filename}.my512"; then
    yetus_del_array_element FILELIST "./${filename}"
    yetus_del_array_element FILELIST "./${filename}.sha512"
    rm "${filename}.my512"
  fi

  # we currently do not verify the mds files
  yetus_del_array_element FILELIST "./${filename}.mds"
done

echo "Following files did not verify:"
echo ""
echo "${FILELIST[*]}"
echo ""

mkdir "${TMPDIR}/unpack"
tar -C "${TMPDIR}/unpack" -xzf "apache-yetus-${NONRC}-src.tar.gz"
pushd "${TMPDIR}/unpack/yetus-project-${NONRC}" || exit 1
mvn clean install


