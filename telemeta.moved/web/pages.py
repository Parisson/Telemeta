from django.conf import settings
import re
import os
import telemeta
import mimetypes

PAGES_ROOT = os.path.join(os.path.dirname(telemeta.__file__), 'pages')

class PageTextContent(object):
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path

    def __iter__(self):
        file = open(self.filename, 'r')
        for line in file:
            yield line.rstrip('\r\n')
        file.close()

    def __unicode__(self):        
        file = open(self.filename, 'r')
        data = file.read()
        file.close()
        return data

class PageAttachment(object):
    def __init__(self, filename, path):
        self.filename = filename
        self.path     = path

    def mimetype(self):
        type, encoding = mimetypes.guess_type(self.filename)
        return type

    def __iter__(self):
        file = open(self.filename, 'rb')
        buffer_size = 0x10000
        while True:
            chunk = file.read(buffer_size)
            yield chunk
            if len(chunk) < buffer_size:
                break

        file.close()

def language_code(request=None):
    code = (request and getattr(request, 'LANGUAGE_CODE', None)) or settings.LANGUAGE_CODE
    cut = re.split('[_-]', code)
    code = cut[0]
    return code.lower()

def project_dir():
    import settings as settings_mod
    if '__init__.py' in settings_mod.__file__:
        p = os.path.dirname(settings_mod.__file__)
    else:
        p = settings_mod.__file__
    project_directory, settings_filename = os.path.split(p)
    if project_directory == os.curdir or not project_directory:
        project_directory = os.getcwd()

    return project_directory        

def resolve_page_file(root, relative_path, ignore_slash_issue=False):
    root = os.path.realpath(root)
    filename = None
    current = root
    is_attachment = False
    for node in relative_path.split('/'):
        if not node:
            continue
        current = os.path.join(current, node)
        rst = current + '.rst'
        if os.path.isfile(rst):
            filename = rst
            break
        elif os.path.isfile(current):
            filename      = current
            is_attachment = True
        elif not os.path.isdir(current):
            break

    if not filename and os.path.isdir(current):
        rst = os.path.join(current, 'index.rst')
        if os.path.isfile(rst):
            if not ignore_slash_issue and relative_path[-1:] != '/':
                raise MalformedPagePath("The relative page os.path must end with a slash when "
                                        "resolving an implicit directory index")
            filename = rst

    if filename:
        filename = os.path.realpath(filename)
        if filename.index(root) != 0:
            filename = None

    if filename:
        if is_attachment:
            return PageAttachment(filename, relative_path)
        else:
            return PageTextContent(filename, relative_path)

    return None

def get_page_content(request, relative_path, ignore_slash_issue=False):     
    lang = language_code(request)
    userroot = os.path.join(project_dir(), 'telemeta-pages')
    rootlist = [os.path.join(userroot, lang), os.path.join(userroot, 'default'), 
                os.path.join(PAGES_ROOT, lang), os.path.join(PAGES_ROOT, 'default')]
    for root in rootlist:
        content = resolve_page_file(root, relative_path, ignore_slash_issue=ignore_slash_issue)
        if content:
            return content

    return None            
    
class MalformedPagePath(Exception):
    pass

