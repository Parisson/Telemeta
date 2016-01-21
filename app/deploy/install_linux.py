#!/usr/bin/python

import os, sys
import argparse

sysvinit_script = """#!/bin/sh

### BEGIN INIT INFO
# Provides:	    %s
# Required-Start:	docker
# Required-Stop:	docker
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	Docker Services
### END INIT INFO

set -e

PROJECT_NAME=%s
YAMLFILE=%s
OPTS="-f $YAMLFILE -p $PROJECT_NAME"
UPOPTS="-d --no-recreate --no-build --no-deps"

. /lib/lsb/init-functions

case "$1" in
    start)
        log_daemon_msg "Starting $PROJECT_NAME composition" "$PROJECT_NAME" || true
        if su -c "docker-compose $OPTS up $UPOPTS > /dev/null 2>&1" root ; then
            log_end_msg 0 || true
        else
            log_end_msg 1 || true
        fi
        ;;

    stop)
        log_daemon_msg "Stopping $PROJECT_NAME composition" "$PROJECT_NAME" || true
        if su -c "docker-compose $OPTS stop > /dev/null 2>&1" root; then
            log_end_msg 0 || true
        else
            log_end_msg 1 || true
        fi
        ;;

    reload|force-reload)
        log_daemon_msg "Reloading $PROJECT_NAME composition" "$PROJECT_NAME" || true
        if docker-compose $OPTS up $UPOPTS > /dev/null 2>&1 ; then
            log_end_msg 0 || true
        else
            log_end_msg 1 || true
        fi
        ;;

    restart|try-restart)
        log_daemon_msg "Restarting $PROJECT_NAME composition" "$PROJECT_NAME" || true
        if docker-compose $OPTS stop > /dev/null 2>&1; docker-compose $OPTS up $UPOPTS > /dev/null 2>&1 ; then
            log_end_msg 0 || true
        else
            log_end_msg 1 || true
        fi
        ;;

    status)
        docker-compose $OPTS ps && exit 0 || exit $?
        ;;

    *)
        log_action_msg "Usage: /etc/init.d/$PROJECT_NAME {start|stop|reload|force-reload|restart|try-restart|status}" || true
        exit 1
        ;;
esac

exit 0
"""

systemd_service = """
[Unit]
Description=%s composition
Requires=docker.service
After=docker.service

[Service]
ExecStart=%s -f %s up -d
ExecStop=%s -f %s stop

[Install]
WantedBy=local.target
"""


class DockerComposeDaemonInstall(object):

    vcs_types = ['git', 'svn', 'hg']
    docker = '/etc/init.d/docker'
    docker_compose = '/usr/local/bin/docker-compose'

    def __init__(self, path=None, init_type='sysvinit'):
        self.init_type = init_type

        self.local_path = os.path.dirname(os.path.realpath(__file__))
        if not path or not os.path.isdir(path):
            self.root = self.get_root(self.local_path)
        else:
            self.root = os.path.abspath(path)

        if self.root[-1] == os.sep:
            self.name = self.root.split(os.sep)[-2].lower()
        else:
            self.name = self.root.split(os.sep)[-1].lower()

        self.conf = self.root + os.sep + 'docker-compose.yml'

    def is_root(self, path):
        content = os.listdir(path)
        for vcs_type in self.vcs_types:
            if '.' + vcs_type in content:
                return True
        return False

    def get_root(self, path):
        while not self.is_root(path):
            path = os.sep.join(path.split(os.sep)[:-1])
        if not path:
            raise ValueError('This is not a versioned repository, please give the root directory of the app as the first argument.')
        return path

    def install_docker(self):
        if not os.path.exists(self.docker):
            print 'Installing docker first...'
            os.system('wget -qO- https://get.docker.com/ | sh')
        if not os.path.exists(self.docker_compose):
            print 'Installing docker-compose...'
            os.system('pip install docker-compose')

    def install_daemon_sysvinit(self):
        service = '/etc/init.d/' + self.name
        print 'Writing sysvinit script in ' + service
        script = sysvinit_script % (self.name, self.name, self.conf)
        f = open(service, 'w')
        f.write(script)
        f.close()
        os.system('chmod 755 ' + service)
        os.system('update-rc.d ' + self.name + ' defaults')

    def install_daemon_systemd(self):
        service = '/lib/systemd/system/' + self.name + '.service'
        print 'Writing systemd service in ' +  service
        conf = systemd_service % (self.name, self.docker_compose, self.conf, self.docker_compose, self.conf)
        f = open(service, 'w')
        f.write(rules)
        f.close()
        os.system('systemctl enable ' + service)
        os.system('systemctl daemon-reload')

    def run(self):
        print 'Installing ' + self.name + ' composition as a daemon...'
        self.install_docker()
        if self.init_type == 'sysvinit':
            self.install_daemon_sysvinit()
        elif self.init_type == 'systemd':
            self.install_daemon_systemd()
        print 'Done'


if __name__ == '__main__':
    path = sys.argv[-1]
    install = DockerComposeDaemonInstall(path)
    install.run()
