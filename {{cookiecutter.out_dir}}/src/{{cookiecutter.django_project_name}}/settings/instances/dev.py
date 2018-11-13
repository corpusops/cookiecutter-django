#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..prod import *

g = set_prod_settings(globals(), 'dev')
globals().update(g)
# vim:set et sts=4 ts=4 tw=80:
