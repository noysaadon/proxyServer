import base64

import requests
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.protobuf.json_format import MessageToDict

from .pokemon_pb2 import _sym_db
from .utils import load_config, match_rule, is_valid_signature


config = load_config()

# Access the symbol database to retrieve the Pokemon message type
Pokemon = _sym_db.GetSymbol('pokedex.Pokemon')


def initialize_stream(url, email, enc_secret):
    stream_start_url = 'https://hiring.external.guardio.dev/be/stream_start'
    request_body = {
        "url": url,
        "email": email,
        "enc_secret": enc_secret
    }

    response = requests.post(stream_start_url, json=request_body)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to start stream: {response.status_code} {response.text}")


@method_decorator(csrf_exempt, name='dispatch')
class StreamView(View):

    def post(self, request, *args, **kwargs):

        signature = request.headers.get('X-Grd-Signature')
        if not signature:
            return JsonResponse({'error': 'Missing signature'}, status=400)

        if not is_valid_signature(request.body, signature):
            return JsonResponse({'error': 'Invalid signature'}, status=401)

        try:
            decoded_body = base64.b64decode(request.body)
            pokemon = Pokemon()
            pokemon.ParseFromString(decoded_body)
            pokemon_dict = MessageToDict(pokemon)
        except Exception as e:
            return JsonResponse({'error': 'Error parsing message'}, status=400)

        # Match the request against the rules
        rule = match_rule(pokemon_dict, config)
        if not rule:
            return JsonResponse({'message': 'No matching rule found'}, status=200)

        # Forward the request
        headers = {**request.headers, 'X-Grd-Reason': rule['reason']}
        response = requests.post(rule['url'], json=pokemon_dict, headers=headers)

        return JsonResponse(response.json(),
                            status=response.status_code,
                            content_type=response.headers.get('Content-Type'))


# BONUS
#class StatsView(View):
#
#    def get(self, request, *args, **kwargs):
#        # Implement metrics collection and return
#        request_count = cache.get('request_count', 0)
#        error_count = cache.get('error_count', 0)
#        incoming_bytes = cache.get('incoming_bytes', 0)
#        outgoing_bytes = cache.get('outgoing_bytes', 0)
#        total_response_time = cache.get('total_response_time', 0.0)
#
#        # Calculate metrics
#        error_rate = error_count / request_count if request_count else 0
#        average_response_time = (total_response_time / request_count) if request_count else 0
#
#        stats = {
#            "request_count": request_count,
#            "error_rate": error_rate,
#            "incoming_bytes": incoming_bytes,
#            "outgoing_bytes": outgoing_bytes,
#            "average_response_time": average_response_time
#        }
#
#        return JsonResponse(stats)
