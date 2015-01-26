# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Parisson SARL

import random, re
from django.db.models import Q
from django.contrib.sites.models import Site


def get_random_hash():
    hash = random.getrandbits(64)
    return "%016x" % hash


def get_full_url(path):
    return 'http://' + Site.objects.get_current().domain + path


def word_search_q(field, pattern):
    words = re.split("[ .*-]+", pattern)
    q = Q()
    for w in words:
        if len(w) >= 3:
            kwargs = {field + '__icontains': w}
            q &= Q(**kwargs)

    return q
