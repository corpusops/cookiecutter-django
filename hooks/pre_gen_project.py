#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys


cache_system = '{{ cookiecutter.cache_system }}'

if cache_system not in ['redis', 'memcached', '', None]:
    sys.exit(1)
# vim:set et sts=4 ts=4 tw=80:
