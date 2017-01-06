# -*- coding: utf-8 -*-
# Shared logging setup

import logging
import sys

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stderr))
