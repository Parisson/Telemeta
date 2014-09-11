#/usr/bin/python

import sys
from telemeta.util.kdenlive.fade import AutoFade

path = sys.argv[-1]
fade = AutoFade(path)
data = fade.run()
f = open(path, 'w')
f.write(data)
f.close()
