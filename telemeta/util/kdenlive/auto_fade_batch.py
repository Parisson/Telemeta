
import os, sys
from telemeta.util.kdenlive.fade import AutoFade

if __name__ == '__main__':
    dir = sys.argv[-2]
    ext = sys.argv[-1]

    for filename in os.listdir(dir):
        prefix, extension = os.path.splitext(filename)
        path = dir + os.sep + filename
        flag = path + '.faded'
        if ext in extension and not os.path.exists(flag):
            os.system('cp ' + path + ' ' + path + '.bak')
            fade = AutoFade(path)
            data = fade.run()
            f = open(path, 'w')
            f.write(data)
            f.close()
            os.system('touch ' + flag)
