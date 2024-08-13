#import time
#from django.core.cache import cache
#from django.utils.deprecation import MiddlewareMixin
#
#
#class MetricsMiddleware(MiddlewareMixin):
#    def process_request(self, request):
#        request.start_time = time.time()
#        # Capture incoming bytes
#        request.incoming_bytes = len(request.body)
#
#    def process_response(self, request, response):
#        response_time = time.time() - getattr(request, 'start_time', time.time())
#
#        # Update cache metrics
#        cache.incr('request_count', 1)
#        cache.incr('incoming_bytes', getattr(request, 'incoming_bytes', 0))
#        cache.incr('outgoing_bytes', len(response.content))
#        cache.incr('total_response_time', response_time)
#
#        if response.status_code >= 400:
#            cache.incr('error_count', 1)
#
#        return response
#
#    def process_exception(self, request, exception):
#        cache.incr('error_count', 1)
#        return None
#