#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ..prod import *
exec('import {0} as outerns'.format(__name__), globals(), locals())
set_prod_settings(outerns)
# Already set in ansible code, only here for example
# hosts = ['0.0.0.0', 'staging.mixity.co', '.mixity.co',]
# CORS_ORIGIN_WHITELIST = CORS_ORIGIN_WHITELIST + tuple(hosts)
# ALLOWED_HOSTS.extend(hosts)
# vim:set et sts=4 ts=4 tw=80:
