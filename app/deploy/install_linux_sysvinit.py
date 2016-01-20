#!/usr/bin/python

import os

path = os.sep.join(os.getcwd().split(os.sep)[:-2])
name = path.split(os.sep)[-1].lower()
conf = path + os.sep + 'docker-compose.yml'
service = '/etc/init.d/' + name

print 'installing ' + name + '...'

if not os.path.exists('/etc/init.d/docker'):
    os.system('wget -qO- https://get.docker.com/ | sh')
    os.system('pip install docker-compose')

f = open('init.sh.example', 'r')
rules = f.read() % (name, name, conf)
f.close()

f = open(service, 'w')
f.write(rules)
f.close()

os.system('chmod 755 ' + service)
os.system('update-rc.d ' + name + ' defaults')

print 'done'
