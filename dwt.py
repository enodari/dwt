import base64
import hashlib
import hmac
import time

MAX_TTL = 60 * 20  # 20 minutes


def _tokenize(key, msg):
    """Build a new token.

    The token consists of the message and its HMAC-SHA256 signature.
    These two parts are Base64url encoded and concatenated by a dot.

    Args:
        key (str): The secret key.
        msg (str): The message.

    Returns:
        str: The generated token.

    """
    key = key.encode('utf-8')
    msg = base64.urlsafe_b64encode(msg.encode('utf-8'))

    sig = hmac.new(key, msg, digestmod=hashlib.sha256).digest()

    return (msg + b'.' + base64.urlsafe_b64encode(sig)).decode('utf-8')


def issue(key, ttl):
    """Issue a token with a limited lifespan.

    Args:
        key (str): The secret key.
        ttl (int): Lifespan in seconds of the new token.

    Returns:
        str: The generated token.

    """
    if ttl < 0 or ttl > MAX_TTL:
        raise ValueError('TTL must be more than 0 and less than ' + MAX_TTL)

    return _tokenize(key, str(time.time() + ttl))


def check(key, tok):
    """Check a token.

    Args:
        key (str): The secret key.
        tok (str): The token to check.

    Returns:
        bool: True if it's correctly signed and not expired. False otherwise.

    """
    try:
        msg = tok.split('.', 2)[0]  # get payload
        msg = base64.urlsafe_b64decode(msg).decode('utf-8')  # decode payload

        return float(msg) > time.time() and tok == _tokenize(key, msg)
    except:  # if something goes wrong always return False.
        return False
