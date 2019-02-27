import base64
import hashlib
import hmac
import time

MAXTTL = 60 * 20  # 20 minutes


def hs256(key, msg):
    key = key.encode('utf-8')
    msg = base64.urlsafe_b64encode(msg.encode('utf-8'))

    sig = hmac.new(key, msg=msg, digestmod=hashlib.sha256).digest()

    return (msg + b'.' + base64.urlsafe_b64encode(sig)).decode('utf-8')


def issue(key, ttl):
    if ttl < 0 or ttl > MAXTTL:
        raise ValueError('TTL must be more than 0 and less than ' + MAXTTL)

    return hs256(key, str(time.time() + ttl))


def check(key, tok):
    try:
        msg = tok.split('.', 2)[0]  # get payload
        msg = base64.urlsafe_b64decode(msg).decode('utf-8')  # decode payload

        return float(msg) > time.time() and tok == hs256(key, msg)
    except:
        return False
