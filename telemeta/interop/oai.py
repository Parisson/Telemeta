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

class ArgumentValidator(object):
    """OAI-PMH request argument validator"""

    def __init__(self, request, response):
        self.response = response
        self.opt_args = []
        self.required_args = ['verb']
        self.request = request
        self.format = None

    def optional(self, *args):
        """Add optional arguments"""
        self.opt_args.extend(args)

    def require(self, *args):
        """Add required arguments"""
        self.required_args.extend(args)

    def accept_format(self, format):
        """Indicate which metadata format is supported"""
        self.format = format

    def has_verb(self):
        """Check if the request includes a valid Verb, return True if it does, False otherwise, 
           setting an error into the response"""

        valid = ['GetRecord', 'Identify', 'ListIdentifiers', 'ListMetadataFormats', 'ListRecords', 'ListSets']

        result = False
        if self.request.has_key('verb'):
            try:
                valid.index(self.request['verb'])
                result = True
            except ValueError:
                pass

        if not result:
            self.response.error('badVerb')

        return result

    def validate(self):
        """Perform validation, return True if successfull, False otherwise, setting appropriate
           errors into the response"""
        all_args    = []
        all_args[:] = self.opt_args[:]
        all_args.extend(self.required_args)
        for k in self.request:
            try:
                all_args.index(k)
            except ValueError:
                self.response.error('badArgument', 'Invalid argument: %s' % k)
                return False

        return self.pre_validate()

    def pre_validate(self):
        """Same as validate(), but doesn't not check for unknown arguments"""

        for k in self.required_args:
            if not self.request.has_key(k):
                self.response.error('badArgument', 'Missing required argument: %s' % k)
                return False

        for k in self.request:
            if k == 'metadataPrefix':
                if self.format:
                    if self.format != self.request[k]:
                        self.response.error('cannotDisseminateFormat')
                        return False
                else:
                    raise Exception('Can\'t validate metadataPrefix argument: supported format isn\'t defined')
            elif (k == 'from') or (k == 'until'):
                try:
                    datetime.strptime(self.request[k], '%Y-%m-%dT%H-%M-%SZ')
                except ValueError:
                    self.response.error('badArgument', "Invalid ISO8601 time format in '%s' argument" % k)
                    return False

        return True         

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

    def parse_time(self, str):
        """Parse an ISO8601 date string into a datetime object"""
        return datetime.strptime(str, '%Y-%m-%dT%H-%M-%SZ')

    def handle(self, args, datasource):
        """Handle a request and return the response as a DOM document"""

        response = Response(self.identity, datasource)

        validator = ArgumentValidator(args, response)
        validator.accept_format('oai_dc')

        if validator.has_verb():

            verb = args['verb']
            response.set_verb(verb)

            if verb == 'Identify':
                validator.validate() and response.identify()
            elif verb == 'GetRecord':
                validator.require('identifier', 'metadataPrefix')
                validator.validate() and response.get_record(args['identifier'])

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
        """Set the verb of the response. Should be called before any 'real' method such
           as identify(), get_record(), etc..."""
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
        """Add error tag using code. If msg is not provided, use a default error message."""

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
        """Build and return a record header"""
        header = self.doc.createElement('header')
        self.append_elements(header, {'identifier': id, 'dateStamp': self.make_time(ctime)})
        return header

    def make_record(self, id, dc, ctime):
        """Build and return a record"""
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
        """Append GetRecord result"""
        record = self.datasource.get_record(id)
        if not record:
            self.error('idDoesNotExist')
        else:
            dc, ctime = record
            self.set_attributes(self.request, {'identifier': id, 'metadataPrefix': 'oai_dc'})
            container = self.root.appendChild(self.doc.createElement(self.verb))
            container.appendChild(self.make_record(id, dc, ctime))
            
    def free(self):
        """Free the resources used by this response"""
        self.doc.unlink()






