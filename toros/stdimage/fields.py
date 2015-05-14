# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import)

import warnings

from . import StdImageField as ModelField


class StdImageField(ModelField):
    def __init__(self, *args, **kwargs):
        super(StdImageField, self).__init__(*args, **kwargs)
        warnings.warn(DeprecationWarning('StdImageField has moved'
                                         ' into a the model module.'))
