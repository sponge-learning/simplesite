from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import TemplateView
import memcache


class Index(TemplateView):
    template_name = 'index.html'
    cache_key = 'count'

    def post(self, request, **kwargs):
        try:
            cache.incr(self.cache_key)
        except ValueError:
            # Cache entry doesn't exist, so create it
            cache._cache.cas(cache.make_key(self.cache_key), 1)
        return redirect('.')

    def get_context_data(self, **kwargs):
        return {
            'count': cache.get(self.cache_key, 0),
        }