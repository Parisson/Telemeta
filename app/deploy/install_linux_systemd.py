#!/usr/bin/python

import os

path = os.sep.join(os.getcwd().split(os.sep)[:-2])
name = path.split(os.sep)[-1].lower()
conf = path + os.sep + 'docker-compose.yml'
program = '/usr/local/bin/docker-compose'
service = '/lib/systemd/system/' + name + '.service'

print 'installing ' + name + '...'

if not os.path.exists('/etc/init.d/docker'):
    os.system('wget -qO- https://get.docker.com/ | sh')
    os.system('pip install docker-compose')

rules="""
[Unit]
Description=%s composition
Requires=docker.service
After=docker.service

[Service]
ExecStart=%s -f %s up -d
ExecStop=%s -f %s stop

[Install]
WantedBy=local.target
""" % (name, program, conf, program, conf)

# print rules

f = open(service, 'w')
f.write(rules)
f.close()

os.system('systemctl enable ' + service)
os.system('systemctl daemon-reload')

print 'done'
