#!/usr/bin/env python

from autoloads import Entity, EntityHelper


class BaseModel(Entity, EntityHelper):
    def __init__(self, **kargs):
        Entity.__init__(self, **kargs)
