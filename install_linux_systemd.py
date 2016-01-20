#!/usr/bin/python

import os

path = os.getcwd()
name = path.split(os.sep)[-1]
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
ExecStart=/usr/local/bin/docker-compose -f %s/docker-compose.yml up -d
ExecStop=/usr/local/bin/docker-compose -f %s/docker-compose.yml stop

[Install]
WantedBy=local.target
""" % (name, path, path)

# print rules

f = open(service, 'w')
f.write(rules)
f.close()

os.system('systemctl enable ' + service)
os.system('systemctl daemon-reload')

print 'done'
