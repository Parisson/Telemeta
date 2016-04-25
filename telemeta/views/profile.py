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


class ProfileView(object):
    """Provide Collections web UI methods"""

    @method_decorator(login_required)
    def profile_detail(self, request, username, template='telemeta/profile_detail.html'):
        user = User.objects.get(username=username)
        try:
            profile = user.get_profile()
        except:
            profile = None
        playlists = get_playlists(request, user)
        user_revisions = get_revisions(25, user)

        return render(request, template, {'profile' : profile, 'usr': user, 'playlists': playlists,
                                          'user_revisions': user_revisions})

    @method_decorator(login_required)
    def profile_edit(self, request, username, template='telemeta/profile_edit.html'):
        if request.user.is_superuser:
            user_hidden_fields = ['profile-user', 'user-password', 'user-last_login', 'user-date_joined']
        else:
            user_hidden_fields = ['user-username', 'user-is_staff', 'profile-user', 'user-is_active',
                         'user-password', 'user-last_login', 'user-date_joined', 'user-groups',
                         'user-user_permissions', 'user-is_superuser', 'profile-expiration_date']

        user = User.objects.get(username=username)
        if user != request.user and not request.user.is_staff:
            mess = ugettext('Access not allowed')
            title = ugettext('User profile') + ' : ' + username + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        try:
            profile = user.get_profile()
        except:
            profile = UserProfile(user=user)

        if request.method == 'POST':
            user_form = UserChangeForm(request.POST, instance=user, prefix='user')
            profile_form = UserProfileForm(request.POST, instance=profile, prefix='profile')
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('telemeta-desk-profile', username)
        else:
            user_form = UserChangeForm(instance=user, prefix='user')
            profile_form = UserProfileForm(instance=profile, prefix='profile')
            forms = [user_form, profile_form]
        return render(request, template, {'forms': forms, 'usr': user,
                                'user_hidden_fields': user_hidden_fields})

