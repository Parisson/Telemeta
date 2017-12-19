# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2012 Parisson SARL

# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *
from saved_searches.models import SavedSearch
from telemeta.views.enum import *

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

        context = RequestContext(request, {
                    'page_content': pages.get_page_content(request,
                    'home', ignore_slash_issue=True),
                    'sound_pub_items': sound_pub_items,
                    'sound_pub_item': sound_pub_item })
        return HttpResponse(template.render(context))

    def lists(self, request, range_playlist):
        """Render the home page"""

        if request.user.is_authenticated():
            template='telemeta/lists.html'
            playlists = get_playlists(request)
            revisions = get_revisions(100)
            user_revisions = get_revisions(25, request.user)
            #if range_playlist is None:
            #    range_playlist = 0
            return render(request, template, {'playlists': playlists,
                                              'revisions': revisions, 'user_revisions': user_revisions , 'last_playlist':range_playlist})
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
