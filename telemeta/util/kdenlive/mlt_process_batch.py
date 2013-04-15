
import os, sys

if __name__ == '__main__':
    dir = sys.argv[-1]

    for filename in os.listdir(dir):
        prefix, extension = os.path.splitext(filename)
        path = dir + os.sep + filename
        flag = path + '.processed'
        if 'sh' in extension and not os.path.exists(flag):
            os.system('nice -n 19 ' + path)
            os.system('touch ' + flag)
