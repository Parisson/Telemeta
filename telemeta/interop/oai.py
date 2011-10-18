# -*- coding: utf-8 -*-
# Generic OAI-PMH Data Provider module
#
# Copyright (C) 2009 Samalyse SARL
# Author: Olivier Guilyardi <olivier samalyse com>
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from datetime import datetime
import time
try:
  import libxml2dom as dom
except ImportError:
    import xml.dom.minidom as dom
    try:
        import libxml2
    except ImportError:
        # dangerous: minidom output formatting isn't very good, libxml2 is much better
        pass

class IDataSource(object):
    """Interface for OAI datasource adapters"""

    def get_earliest_time(self):
        """Must return the change time of the oldest record(s) as a datetime object"""
        pass

    def get_record(self, id):
        """Must return a tuple of the form:
              (
                [(dublin core element, element value), ...],
                change time
              )
           or None if the record doesn't exist. In case the id isn't wellformed
           a BadArgumentError should be raised.

           The dublin core data must contain an 'identifier' element, which is the same
           as the id parameter."""
        pass

    def count_records(self, from_time = None, until_time = None):
        """Must return the number of records between (optional) from and until change time."""
        pass

    def list_records(self, offset, limit, from_time = None, until_time = None):
        """Must return the list of records between (optional) from and
           until change time, starting from record at offset, with a maximum of limit
           entries. Each entry of the list must be a tuple of the same form as returned
           by getRecord().

           If no record matches, should return an empty list. The dublin core data must
           contain an 'identifier' element, which can be used as a parameter to get_record()."""
        pass

def iso_time(date_time = None):
    """Encode a datetime object using ISO8601 format"""
    if not date_time:
        date_time = datetime.now()
    return date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

def parse_iso_time(str):
    """Parse an ISO8601 time string into a datetime object, or return None on failure"""
    # Avoid datetime.strptime() for compatibility with python < 2.5
    try:
        s = time.strptime(str, '%Y-%m-%dT%H:%M:%SZ')
        return datetime(s.tm_year, s.tm_mon, s.tm_mday, s.tm_hour, s.tm_min, s.tm_sec)
    except ValueError:
        try:
            s = time.strptime(str, '%Y-%m-%d')
            return datetime(s.tm_year, s.tm_mon, s.tm_mday)
        except ValueError:
            return None

def doc_to_string(doc):
    if dom.__name__ == 'libxml2dom':
        return doc.toString(encoding='utf-8', prettyprint=True).decode('utf-8')
    try:
        doc2 = libxml2.parseDoc(doc.toxml(encoding="utf-8"))
        xml = unicode(doc2.serialize(encoding="utf-8", format=1), "utf-8")
        doc2.free()
        return xml
    except NameError:
        return doc.toprettyxml(encoding="utf-8")

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
                if (k == 'set'):
                    self.response.error('noSetHierarchy')
                    return False
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
                if not parse_iso_time(self.request[k]):
                    self.response.error('badArgument', "Invalid ISO8601 time format in '%s' argument" % k)
                    return False

        return True

class DataProvider(object):
    """OAI-PMH Data Provider"""

    max_records_per_response = 500

    def __init__(self, datasource, repository_name, base_url, admin_email):
        self.datasource = datasource
        self.identity = [
            ('repositoryName',   repository_name),
            ('baseURL',          base_url),
            ('protocolVersion',  '2.0'),
            ('adminEmail',       admin_email),
            ('deletedRecord',    'no'),
            ('granularity',      'YYYY-MM-DDThh:mm:ssZ')
        ]

    def parse_time_range(self, args):
        if args.get('from'):
            from_time = parse_iso_time(args['from'])
        else:
            from_time = None
        if args.get('until'):
            until_time = parse_iso_time(args['until'])
        else:
            until_time = None

        return from_time, until_time

    def handle(self, args):
        """Handle a request and return the response as a DOM document"""

        response = Response(self.identity, self.datasource)
        response.max_records_per_response = self.max_records_per_response

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
            elif verb == 'ListIdentifiers' or verb == 'ListRecords':
                validator.optional('metadataPrefix', 'from', 'until', 'set', 'resumptionToken')
                from_time, until_time = self.parse_time_range(args)
                token = args.get('resumptionToken')
                if validator.validate():
                    response.list_records(from_time, until_time, token, ids_only = (verb == 'ListIdentifiers'))
            elif verb == 'ListSets':
                validator.optional('resumptionToken')
                validator.validate() and response.error('noSetHierarchy')
            elif verb == 'ListMetadataFormats':
                validator.optional('identifier')
                validator.validate() and response.list_formats(args.get('identifier'))

        xml = doc_to_string(response.doc)
        response.free()
        return xml

class Response(object):
    """OAI-PMH response generation"""

    max_records_per_response = 500

    def __init__(self, identity, datasource):
        self.identity = identity
        self.datasource = datasource

        impl = dom.getDOMImplementation()
        self.doc = impl.createDocument(None, 'OAI-PMH', None)
        self.root = self.doc.firstChild
        self.root.setAttribute('xmlns', 'http://www.openarchives.org/OAI/2.0/')
        self.root.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        self.root.setAttribute('xsi:schemaLocation', 'http://www.openarchives.org/OAI/2.0/ '
                                                     'http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd')
        self.append_elements(self.root, {'responseDate': iso_time()})
        self.request = self.root.appendChild(self.doc.createElement('request'))
        for k, v in self.identity:
            if k == 'baseURL':
                url = v
                break
        self.request.appendChild(self.doc.createTextNode(url))

    def append_elements(self, parent, elements, prefix=None):
        """Append several elements to parent. elements must either be a tag:value dict or
           an ordered list of (tag, value) tuples."""
        for item in elements:
            if isinstance(item, tuple):
                tag, value = item
            else:
                tag = item
                value = elements[tag]
            if prefix:
                tag = prefix + ':' + tag
            e = parent.appendChild(self.doc.createElement(tag))
            e.appendChild(self.doc.createTextNode(value))
        return parent

    def set_attributes(self, element, attributes):
        """Set several attributes on element, from dict. attributes must either be an
           attr:value dict or an ordered list of (attr, value) tuples. If element is a
           string, then create an element with than name. Return (possibly created)
           element."""
        if isinstance(element, basestring):
            element = self.doc.createElement(element)
        for item in attributes:
            if isinstance(item, tuple):
                attr, value = item
            else:
                attr = item
                value = attributes[item]
            element.setAttribute(attr, value)
        return element

    def set_verb(self, verb):
        """Set the verb of the response. Should be called before any 'real' method such
           as identify(), get_record(), etc..."""
        self.verb = verb
        self.request.setAttribute('verb', self.verb)

    def identify(self):
        """Append Identify tag and child nodes"""

        identity = []
        identity[:] = self.identity[:]
        earliest = self.datasource.get_earliest_time()
        identity.insert(4, ('earliestDatestamp', iso_time(earliest)))

        group = self.root.appendChild(self.doc.createElement('Identify'))
        self.append_elements(group, identity)

    def error(self, code, msg = None):
        """Add error tag using code. If msg is not provided, use a default error message."""

        msgs = {
            'badArgument':              'Incorrect arguments',
            'badResumptionToken':       'Invalid resumption token',
            'badVerb':                  'Illegal OAI verb',
            'noSetHierarchy':           'This repository does not support sets.',
            'idDoesNotExist':           'No such record',
            'cannotDisseminateFormat':  'Unsupported metadata format',
            'noRecordsMatch':           'The request returned an empty record set'
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
        self.append_elements(header, [('identifier', id), ('datestamp', iso_time(ctime))])
        return header

    def make_record(self, id, dc, ctime):
        """Build and return a record"""
        record = self.doc.createElement('record')
        header = record.appendChild(self.make_record_header(id, ctime))
        metadata = record.appendChild(self.doc.createElement('metadata'))
        container = metadata.appendChild(self.doc.createElement('oai_dc:dc'))
        self.set_attributes(container, [
          ('xmlns:oai_dc',       "http://www.openarchives.org/OAI/2.0/oai_dc/"),
          ('xmlns:dc',           "http://purl.org/dc/elements/1.1/"),
          ('xmlns:xsi',          "http://www.w3.org/2001/XMLSchema-instance"),
          ('xsi:schemaLocation', "http://www.openarchives.org/OAI/2.0/oai_dc/ "
                                 "http://www.openarchives.org/OAI/2.0/oai_dc.xsd")
        ])
        self.append_elements(container, dc, prefix='dc')
        return record

    def parse_dc(self, data):
        valid = ['title', 'creator', 'subject', 'description', 'publisher', 'contributor',
                 'date', 'type', 'format', 'identifier', 'source', 'language', 'relation',
                 'coverage', 'rights']

        parsed = []
        id = None
        for k, v in data:
            try:
                valid.index(k)
                parsed.append((k, v))
                if k == 'identifier':
                    id = v
            except ValueError:
                pass

        return id, parsed


    def get_record(self, id):
        """Append GetRecord result"""
        try:
            record = self.datasource.get_record(id)
        except BadArgumentError, e:
            self.error('badArgument', e.message)
            return
        if not record:
            self.error('idDoesNotExist')
        else:
            dc, ctime = record
            dc_id, dc = self.parse_dc(dc)
            if dc_id == None:
                raise Exception("DataSource.get_record() didn't provide an 'identifier' dublin core element")
#            elif dc_id != id:
#                raise Exception("DataSource.get_record() returned an 'identifier' dublin core element "
#                                "which is different from the requested identifier")

            self.set_attributes(self.request, {'identifier': id, 'metadataPrefix': 'oai_dc'})
            container = self.root.appendChild(self.doc.createElement(self.verb))
            container.appendChild(self.make_record(id, dc, ctime))

    def format_id_header(self, id):
        organization = self.identity[0][1] 
        if 'http' in id:
            id = id.split('/')[-1]
        return ':'.join(['oai', organization.lower(), 'items', id])
    
    def list_records(self, from_time, until_time, token = None, ids_only = False):
        """Append ListIdentifiers or ListRecords result"""
        offset = 0
        if token:
            self.request.setAttribute('resumptionToken', token)
            try:
                from_time, until_time, offset = token.split(',')
            except ValueError:
                self.error('badResumptionToken')
                return

            if len(from_time):
                from_time = parse_iso_time(from_time)
                if not from_time:
                    self.error('badResumptionToken')
                    return
            else:
                from_time = None

            if len(until_time):
                until_time = parse_iso_time(until_time)
                if not until_time:
                    self.error('badResumptionToken')
                    return
            else:
                until_time = None

            try:
                offset = int(offset)
            except ValueError:
                self.error('badResumptionToken')
                return
        else:
            if from_time:
                self.request.setAttribute('from', iso_time(from_time))
            if until_time:
                self.request.setAttribute('until', iso_time(until_time))

        count = self.datasource.count_records(from_time, until_time)
        data = self.datasource.list_records(offset, self.max_records_per_response, from_time, until_time)
        if (len(data) > self.max_records_per_response):
            raise Exception("DataSource.list_records() returned too many records")

        if len(data):
            container = self.root.appendChild(self.doc.createElement(self.verb))
            for item in data:
                dc, ctime = item
                id, dc = self.parse_dc(dc)
                id = self.format_id_header(id)
                if id == None:
                    raise Exception("DataSource.list_records() didn't provide an 'identifier' dublin core element")

                if ids_only:
                    container.appendChild(self.make_record_header(id, ctime))
                else:
                    container.appendChild(self.make_record(id, dc, ctime))

            if count - offset > self.max_records_per_response:
                token = container.appendChild(self.doc.createElement('resumptionToken'))
                token.setAttribute('completeListSize', str(count))

                if from_time:
                    from_time = iso_time(from_time)
                else:
                    from_time = ''

                if until_time:
                    until_time = iso_time(until_time)
                else:
                    until_time = ''

                token_str = "%s,%s,%d" % (from_time, until_time, offset + len(data))
                token.appendChild(self.doc.createTextNode(token_str))
            elif offset:
                token = container.appendChild(self.doc.createElement('resumptionToken'))
                token.setAttribute('completeListSize', str(count))
        else:
            self.error("noRecordsMatch")

    def list_formats(self, id = None):
        """Append ListMetadataFormats result"""
        if id:
            record = self.datasource.get_record(id)
            if not record:
                self.error('idDoesNotExist')
                return
            self.request.setAttribute('identifier', id)

        container = self.root.appendChild(self.doc.createElement(self.verb))
        format = container.appendChild(self.doc.createElement('metadataFormat'))
        self.append_elements(format, [
            ('metadataPrefix',       'oai_dc'),
            ('schema',               'http://www.openarchives.org/OAI/2.0/oai_dc.xsd'),
            ('metadataNamespace',    'http://www.openarchives.org/OAI/2.0/oai_dc/')
        ])

    def free(self):
        """Free the resources used by this response"""
        try:
            self.doc.unlink()
        except AttributeError:
            # Apparently no free/unlink method in libxml2dom
            pass

class BadArgumentError(Exception):
    pass
