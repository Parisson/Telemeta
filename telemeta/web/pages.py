from django.conf import settings
import re
import telemeta
from os import path
import mimetypes

PAGES_ROOT = path.join(path.dirname(telemeta.__file__), 'pages')

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
    code = (request and getattr(request, 'LANGUAGE_CODE')) or settings.LANGUAGE_CODE
    cut = re.split('[_-]', code)
    code = cut[0]
    return code.lower()

def resolve_page_file(language_code, relative_path, ignore_slash_issue=False):
    root = path.realpath(path.join(PAGES_ROOT, language_code))
    filename = None
    current = root
    is_attachment = False
    for node in relative_path.split('/'):
        if not node:
            continue
        current = path.join(current, node)
        rst = current + '.rst'
        if path.isfile(rst):
            filename = rst
            break
        elif path.isfile(current):
            filename      = current
            is_attachment = True
        elif not path.isdir(current):
            break

    if not filename and path.isdir(current):
        rst = path.join(current, 'index.rst')
        if path.isfile(rst):
            if not ignore_slash_issue and relative_path[-1:] != '/':
                raise MalformedPagePath("The relative page path must end with a slash when "
                                        "resolving an implicit directory index")
            filename = rst

    if filename:
        filename = path.realpath(filename)
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
    return resolve_page_file(lang, relative_path) or resolve_page_file('default', relative_path)
    
class MalformedPagePath(Exception):
    pass

