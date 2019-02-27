# dwt
Generate and check HMAC-SHA256 expiring tokens.

It's similar to [JWT](https://jwt.io/), but:

 - HS256 only.
 - no header.
 - no payload, only a short expiration time.

So why I made it? It was fun. It's not meant to be used in a production environment.

### Installation
```bash
$ git clone https://github.com/enodari/dwt.git && cd dwt/
$ pip install -e .
```

### Usage Example
```.py
import dwt

KEY = 'you-should-use-a-long-key'

token = dwt.issue(KEY, ttl=5)
dwt.check(KEY, token)
```

[Remember to always use a strong key (256-bit minimum).](https://github.com/brendan-rius/c-jwt-cracker)

### SSO demo
You can use dwt to issue and check tokens for a simple, single-user (clearly not production ready) SSO client/server.

```.py
import dwt

from flask import Flask, make_response, redirect, request

KEY = 'you-should-use-a-long-key'

app = Flask('app')  # run this app on port 8000
sso = Flask('sso')  # run this app on port 5000


@app.route('/')
def hello_world():
    token = request.cookies.get('token')

    if not dwt.check(KEY, token):
        return redirect('http://127.0.0.1:5000/?next=http://127.0.0.1:8000')

    return 'Hello, World!'


@sso.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if request.form.get('pass', '') == 'TEST':
            response = make_response(redirect(request.form.get('next', '')))
            response.set_cookie('token', dwt.issue(KEY, ttl=60))  # expires in a minute

            return response

    return '''<form method=POST>
                  <input type=password name=pass>
                  <input type=hidden name=next value={}>
                  <input type=submit value=go>
              </form>'''.format(request.args.get('next'))
```

### License
[MIT](https://opensource.org/licenses/MIT)
