from enum import Enum

from .decorators import invalidates_cache
from .domain import Filter
from .exceptions import InvalidFilterError


class PaginatedQuerySetMixin:

    @property
    def links(self):
        if not self.has_data:
            return None

        if 'links' not in self._data:
            return None
        return self._data['links']

    @property
    def next_url(self):
        links = self.links
        if links and 'next' in self.links:
            return links['next']
        return None

    @property
    def prev_url(self):
        links = self.links
        if links and 'prev' in self.links:
            return links['prev']
        return None

    @invalidates_cache
    def limit(self, value):
        self.endpoint.args['page[limit]'] = value
        return self

    @invalidates_cache
    def offset(self, value):
        self.endpoint.args['page[offset]'] = value
        return self

    def next(self):
        if not self.has_data:
            return self

        next_url = self.next_url
        if next_url:
            self.endpoint = next_url
            self._data = None
        else:
            self._data['data'] = []
        return self

    def prev(self):
        if not self.has_data:
            return self

        prev_url = self.prev_url
        if prev_url:
            self.endpoint = prev_url
            self._data = None
        else:
            self._data['data'] = []
        return self


class SortableQuerySetMixin:

    @invalidates_cache
    def sort(self, sort_key, ascending=True):
        sort_key = sort_key if ascending else '-{}'.format(sort_key)
        self.endpoint.args['sort'] = sort_key
        return self


class FilterableQuerySetMixin:

    @invalidates_cache
    def filter(self, filter_key, filter_value):
        if not isinstance(filter_key, Filter):
            raise InvalidFilterError("Invalid Filter")
        if isinstance(filter_value, Enum):
            filter_value = filter_value.value

        self.endpoint.args['filter[{}]'.format(
            filter_key.value)] = filter_value
        return self
