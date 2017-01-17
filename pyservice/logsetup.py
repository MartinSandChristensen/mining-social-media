# -*- coding: utf-8 -*-
# Shared logging setup

import inspect
import logging
import sys

log = logging.getLogger(inspect.stack()[1][1].rstrip('.py'))
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)
