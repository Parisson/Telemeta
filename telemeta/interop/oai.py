from xml.dom.minidom import getDOMImplementation
from datetime import datetime
import libxml2

class IDataSource(object):
    """Interface for OAI datasource adapters"""

    def get_earliest_time(self):
        """Must return the change time of the oldest record(s) as a datetime object"""
        pass

    def get_record(self, id):
        """Must return a tuple with :
             - record as (dict,timestamp) of Dublin Core elements
             - last changetime as a datetime object
           or None if the record doesn't exist"""
        pass

class DataProvider(object):
    """OAI-PMH Data Provider"""

    def __init__(self, repository_name, base_url, admin_email):
        self.identity = {
            'repositoryName':   repository_name,
            'baseURL':          base_url,
            'adminEmail':       admin_email,
            'protocolVersion':  '2.0',
            'deletedRecord':    'no',
            'granularity':      'YYYY-MM-DDThh:mm:ssZ'
        }

    def require_argument(self, response, args, required):
        if not args.has_key(required):
            response.error("badArgument", msg="Missing required argument '%s'" % required)
            return False
        return True

    def validate_format(self, response, args):
        arg = args.get('metadataPrefix')
        if not self.require_argument(response, args, 'metadataPrefix'):
            return False
        if arg != 'oai_dc':
            response.error('cannotDisseminateFormat')
            return False

        return True            

    def handle(self, args, datasource):
        """Handle a request and return the response as a DOM document"""
        response = Response(self.identity, datasource)
        if self.require_argument(response, args, 'verb'):
            verb = args.get('verb')
            response.set_verb(verb)
            if verb == 'Identify':
                response.identify()
            elif verb == 'GetRecord':
                if self.require_argument(response, args, 'identifier') and self.validate_format(response, args):
                    response.get_record(args['identifier'])
            else:
                response.error('badVerb')

        doc = libxml2.parseDoc(response.doc.toxml(encoding="utf-8"))
        response.free()
        xml = unicode(doc.serialize(encoding="utf-8", format=1), "utf-8")
        doc.free()
        return xml

class Response(object):
    """OAI-PMH response generation"""

    def __init__(self, identity, datasource):
        self.identity = identity
        self.datasource = datasource

        impl = getDOMImplementation()
        self.doc = impl.createDocument(None, 'OAI-PMH', None)
        self.root = self.doc.firstChild
        self.root.setAttribute('xmlns', 'http://www.openarchives.org/OAI/2.0/')
        self.root.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        self.root.setAttribute('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ '
                                                     'http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')
        self.append_elements(self.root, {'responseDate': self.make_time()})
        self.request = self.root.appendChild(self.doc.createElement('request'))
        self.request.appendChild(self.doc.createTextNode(self.identity['baseURL']))

    def append_elements(self, parent, dict, prefix=None):
        """Append several elements to parent use dict key as tag names and values as text nodes.
           Return the parent."""
        for k in dict:
            if prefix:
                tag = prefix + ':' + k
            else:
                tag = k
            e = parent.appendChild(self.doc.createElement(tag))
            e.appendChild(self.doc.createTextNode(dict[k]))
        return parent

    def set_attributes(self, element, dict):
        """Set several attributes on element, from dict. If element is a string, then create
           an element with than name. Return (possibly created) element."""
        if isinstance(element, basestring):
            element = self.doc.createElement(element)
        for k in dict:
            element.setAttribute(k, dict[k])
        return element

    def set_verb(self, verb):
        self.verb = verb
        self.request.setAttribute('verb', self.verb)

    def identify(self):
        """Append Identify tag and child nodes"""

        identity = self.identity.copy()
        earliest = self.datasource.get_earliest_time()
        identity['earliestDatestamp'] = self.make_time(earliest)

        group = self.root.appendChild(self.doc.createElement('Identify'))
        self.append_elements(group, identity)

    def make_time(self, date_time = None):
        """Encode a datetime object using ISO8601 format"""
        if not date_time:
            date_time = datetime.now()
        return date_time.strftime('%Y-%m-%dT%H-%M-%SZ')


    def error(self, code, msg = None):
        """Add error tag"""

        msgs = {
            'badArgument':              'Incorrect arguments',
            'badVerb':                  'Illegal OAI verb',
            'noSetHierarchy':           'This repository does not support sets.',
            'idDoesNotExist':           'No such record',
            'cannotDisseminateFormat':  'Unsupported metadata format',
        }

        if not msg:
            msg = msgs[code]
            if not msg:
                raise Exception("No such error code: %s" % code)

        err = self.root.appendChild(self.set_attributes('error', {'code': code}))
        err.appendChild(self.doc.createTextNode(msg))

    def make_record_header(self, id, ctime):
        header = self.doc.createElement('header')
        self.append_elements(header, {'identifier': id, 'dateStamp': self.make_time(ctime)})
        return header

    def make_record(self, id, dc, ctime):
        record = self.doc.createElement('record')
        header = record.appendChild(self.make_record_header(id, ctime))
        metadata = record.appendChild(self.doc.createElement('metadata'))
        container = metadata.appendChild(self.doc.createElement('oai_dc'))
        self.set_attributes(container, {
          'xmlns:oai_dc':       "http://www.openarchives.org/OAI/2.0/oai_dc/",
          'xmlns:dc':           "http://purl.org/dc/elements/1.1/",
          'xmlns:xsi':          "http://www.w3.org/2001/XMLSchema-instance",
          'xsi:schemaLocation': "http://www.openarchives.org/OAI/2.0/oai_dc/ "
                                "http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
        })
        self.append_elements(container, dc, prefix='dc')
        return record

    def get_record(self, id):

        record = self.datasource.get_record(id)
        if not record:
            self.error('idDoesNotExist')
        else:
            dc, ctime = record
            self.set_attributes(self.request, {'identifier': id, 'metadataPrefix': 'oai_dc'})
            container = self.root.appendChild(self.doc.createElement(self.verb))
            container.appendChild(self.make_record(id, dc, ctime))

            
    def free(self):
        self.doc.unlink()






