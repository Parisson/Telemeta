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

