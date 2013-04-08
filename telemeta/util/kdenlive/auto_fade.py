
import sys
from telemeta.util.kdenlive.fade import AutoFade

if __name__ == '__main__':
    path = sys.argv[-1]
    fade = AutoFade(path)
    data = fade.run()
    f = open(path, 'w')
    f.write(data)
    f.close()


