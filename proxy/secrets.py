import hmac
import hashlib
import base64

# Secret key
secret_key = 'pokemon_proxy'  # replace with your actual secret key
secret_key_b = b'pokemon_proxy'
data = b'http://hiring.external.guardio.dev/stream'  # replace with actual data you want to hash


def get_base64_form_str():
    b = base64.b64encode(bytes(secret_key, 'utf-8'))  # bytes
    return b.decode('utf-8')


def get_hash_key():
    # HMAC object using SHA256
    hmac_object = hmac.new(secret_key_b, data, hashlib.sha256)

    # Get the raw HMAC bytes
    hmac_digest = hmac_object.digest()

    # Base64 encode the HMAC
    enc_secret = base64.b64encode(hmac_digest).decode('utf-8')

    return enc_secret


secret_key_base64 = get_base64_form_str()

HMAC_SECRET = get_hash_key()
