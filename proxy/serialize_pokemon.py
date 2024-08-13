import base64
import hmac
import hashlib
import requests
from pokemon_pb2 import _sym_db

secret_key_b = b'pokemon_proxy'

Pokemon = _sym_db.GetSymbol('pokedex.Pokemon')

# Create a Pokemon instance
pokemon = Pokemon()
pokemon.number = 25
pokemon.name = "Pikachu"
pokemon.type_one = "Electric"
pokemon.type_two = ""
pokemon.total = 320
pokemon.hit_points = 35
pokemon.attack = 55
pokemon.defense = 40
pokemon.special_attack = 50
pokemon.special_defense = 50
pokemon.speed = 90
pokemon.generation = 1
pokemon.legendary = False

# Serialize the protobuf message to binary
binary_data = pokemon.SerializeToString()
body = base64.b64encode(binary_data)

# Calculate the HMAC-SHA256 signature directly from the binary data
signature = hmac.new(secret_key_b, body, hashlib.sha256).digest()

# Base64 encode the resulting HMAC signature
signature_base64 = base64.b64encode(signature).decode('utf-8')

headers = {
    'X-Grd-Signature': signature_base64
}

# Send the request to the proxy service
response = requests.post('http://localhost:8000/stream/', data=body.decode('utf-8'), headers=headers)


# Print the base64-encoded HMAC signature
print("Signature:", signature_base64)
print("Base64 Encoded Binary Data:", body.decode('utf-8'))
