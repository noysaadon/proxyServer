import base64
import hashlib
import hmac
import json
import operator
from proxy.secrets import secret_key_base64
from reverse_proxy.settings import POKEPROXY_CONFIG


def load_config():
    with open(POKEPROXY_CONFIG, 'r') as config_file:
        return json.load(config_file)


OPS = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
}


def evaluate_expression(field_value, operator_str, value):
    if operator_str not in OPS:
        raise ValueError(f"Unsupported operator: {operator_str}")

    op = OPS[operator_str]
    try:
        value = int(value)
    except ValueError:
        pass

    if isinstance(field_value, str) and value == int(value):
        field_value = int(field_value)

    return op(field_value, value)


def is_valid_signature(body, signature):
    secret = base64.b64decode(secret_key_base64)  # Replace with your secret
    expected_signature = hmac.new(secret, body, hashlib.sha256).digest()
    expected_signature_base64 = base64.b64encode(expected_signature).decode('utf-8')
    return hmac.compare_digest(signature, expected_signature_base64)


def match_rule(pokemon, config):
    pokemon_dict = {key.lower(): value for key, value in pokemon.items()}
    for rule in config["rules"]:
        if matches(pokemon_dict, rule['match']):
            return rule
    return None


def matches(pokemon_dict, match_conditions):
    """
    Match the request body against the given conditions.
    """
    for condition in match_conditions:
        field, operator, value_config = parse_condition(condition)
        field_value_pokemon = pokemon_dict.get(field)
        if not evaluate_condition(field_value_pokemon, operator, value_config):
            return False
    return True


def parse_condition(condition):
    """
    Parse a condition into field, operator, and value.
    """
    for op in ('==', '!=', '>', '<'):
        if op in condition:
            field, value = condition.split(op, 1)
            field = field.replace('_', '').lower().strip()
            return field, op.strip(), value.strip()
    raise ValueError(f"Invalid condition: {condition}")


def evaluate_condition(field_value_pokemon, operator, value_config):
    """
    Evaluate a single condition.
    """
    if operator == '==':
        return field_value_pokemon == value_config
    elif operator == '!=':
        return field_value_pokemon != value_config

    field_value_pokemon_float = to_float(field_value_pokemon)
    value_config_float = to_float(value_config)

    if field_value_pokemon_float is None or value_config_float is None:
        return False

    return (field_value_pokemon_float > value_config_float) if operator == '>' else (
                field_value_pokemon_float < value_config_float) if operator == '<' else False


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
