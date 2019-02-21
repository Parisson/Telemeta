#!/usr/bin/python

import os, sys

if __name__ == '__main__':
    root_dir = sys.argv[-1]

    fading = False
    if '--fading' in sys.argv:
        fading = True

    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            prefix, extension = os.path.splitext(filename)
            path = root + os.sep + filename

            flag = path + '.processed'
            if 'sh' in extension and not os.path.exists(flag):
                if fading:
                    from telemeta.util.kdenlive.fade import AutoFade
                    local_files = os.listdir(root)
                    for local_file in local_files:
                        local_name, local_ext = os.path.splitext(local_file)
                        if 'mlt' in local_ext:
                            local_path = root + os.sep + local_file
                            local_flag = local_path + '.faded'
                            if not os.path.exists(local_flag):
                                print 'fading :	' + local_path 
                                os.system('cp ' + local_path + ' ' + local_path + '.bak')
                                fade = AutoFade(local_path)
                                data = fade.run()
                                f = open(local_path, 'w')
                                f.write(data)
                                f.close()
                                os.system('touch ' + local_flag)

                print 'processing :	' + path
                os.system('nice -n 19 ' + path)
                os.system('touch ' + flag)
