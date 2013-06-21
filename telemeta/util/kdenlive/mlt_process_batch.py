
import os, sys

if __name__ == '__main__':
    root_dir = sys.argv[-1]

    fading = False
    if '--fade' in sys.argv:
        fading = True

    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            prefix, extension = os.path.splitext(filename)
            path = root + os.sep + filename

            flag = path + '.faded'
            if 'mlt' in extension and not os.path.exists(flag) and fading:
                from telemeta.util.kdenlive.fade import AutoFade
                fade = AutoFade(path)
                data = fade.run()
                f = open(path, 'w')
                f.write(data)
                f.close()
                os.system('touch ' + flag)

            flag = path + '.processed'
            if 'sh' in extension and not os.path.exists(flag):
                os.system('nice -n 19 ' + path)
                os.system('touch ' + flag)
