# Copyright 2013 Thatcher Peskens
# Copyright 2014, 2017 Guillaume Pellerin, Thomas Fillon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM parisson/timeside:latest-dev

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>, Thomas fillon <thomas@parisson.com>

RUN mkdir -p /srv/lib/
RUN mkdir -p /srv/app
RUN mkdir -p /srv/media
RUN mkdir -p /srv/lib/telemeta

RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y --force-yes mysql-client

COPY . /srv/lib/telemeta
WORKDIR /srv/lib/telemeta

# Install Timeside and plugins from ./lib
COPY ./app/bin/setup_plugins.sh /srv/app/bin/setup_plugins.sh
COPY ./lib/plugins/ /srv/lib/plugins/
RUN /bin/bash /srv/app/bin/setup_plugins.sh

# Install Telemeta
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt --src /srv/lib
RUN pip uninstall -y south

WORKDIR /srv/app
EXPOSE 8000
