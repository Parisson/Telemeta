# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2012 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

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

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *
from saved_searches.models import SavedSearch


class HomeView(object):
    """Provide general web UI methods"""

    def home(self, request):
        """Render the index page"""

        template = loader.get_template('telemeta/home.html')

        N = 3   # max number of pub items

        sound_items = MediaItem.objects.sound_public()
        count = sound_items.count()

        if count == 0:
            sound_pub_item = None
            sound_pub_items = None

        elif count == 1:
            sound_pub_item = sound_items[0]
            sound_pub_items = [sound_items[0], sound_items[0]]

        elif count == 2:
            sound_pub_item = sound_items[0]
            sound_pub_items = [sound_items[0], sound_items[1]]

        elif count > 2:
            indexes = random.sample(range(count-1), N)
            sound_pub_item = sound_items[indexes[0]]
            sound_pub_items = [sound_items[indexes[i]] for i in range(1, N)]

        revisions = get_revisions(25)
        context = RequestContext(request, {
                    'page_content': pages.get_page_content(request, 'home', ignore_slash_issue=True),
                    'revisions': revisions,  'sound_pub_items': sound_pub_items,
                    'sound_pub_item': sound_pub_item })
        return HttpResponse(template.render(context))

    def lists(self, request):
        """Render the home page"""

        if request.user.is_authenticated():
            template='telemeta/lists.html'
            playlists = get_playlists(request)
            revisions = get_revisions(100)
            user_revisions = get_revisions(25, request.user)
            return render(request, template, {'playlists': playlists,
                                              'revisions': revisions, 'user_revisions': user_revisions })
        else:
            template = 'telemeta/messages.html'
            mess = ugettext('Access not allowed')
            title = ugettext('Lists') + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, template, {'description' : description})

    def handle_oai_request(self, request):
        host = request.META['HTTP_HOST']
        datasource  = TelemetaOAIDataSource()
        repository_name = settings.TELEMETA_ORGANIZATION
        url         = 'http://' + host + request.path
        admin       = settings.ADMINS[0][1]
        provider    = oai.DataProvider(datasource, repository_name, url, admin)
        args        = request.GET.copy()
        args.update(request.POST)
        return HttpResponse(provider.handle(args), mimetype='text/xml')

    def render_flatpage(self, request, path):
        try:
            content = pages.get_page_content(request, path)
        except pages.MalformedPagePath:
            return redirect(request.path + '/')

        if isinstance(content, pages.PageAttachment):
            return HttpResponse(content, content.mimetype())
        else:
            return render(request, 'telemeta/flatpage.html', {'page_content': content })

    def logout(self, request):
        auth.logout(request)
        return redirect('telemeta-home')

    def complete_location(self, request, with_items=True):
        input = request.REQUEST

        token = input['q']
        limit = int(input['limit'])
        if with_items:
            locations = MediaItem.objects.all().locations()
        else:
            locations = Location.objects.all()

        locations = locations.filter(name__istartswith=token).order_by('name')[:limit]
        data = [unicode(l) + " (%d items)" % l.items().count() for l in locations]

        return HttpResponse("\n".join(data))

    @method_decorator(login_required)
    def users(self, request):
        users = User.objects.all().order_by('last_name')
        return render(request, 'telemeta/users.html', {'users': users})
