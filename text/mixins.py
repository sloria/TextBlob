# -*- coding: utf-8 -*-
from __future__ import absolute_import
from text.compat import basestring

class ComparableMixin(object):

    '''Implements rich operators for an object.'''

    def _compare(self, other, method):
        try:
            return method(self._cmpkey(), other._cmpkey())
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other". Try the reverse comparison
            return NotImplemented

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)


class BlobComparableMixin(ComparableMixin):

    '''Allow blob objects to be comparable with both strings and blobs.'''

    def _compare(self, other, method):
        if isinstance(other, basestring):
            # Just compare with the other string
            return method(self._cmpkey(), other)
        return super(BlobComparableMixin, self)._compare(other, method)
