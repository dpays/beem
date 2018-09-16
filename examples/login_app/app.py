from flask import Flask, request
from dpaygo.dpayid import DPayId
import getpass

app = Flask(__name__)


c = DPayId(client_id="dpaygo.app", scope="login,vote,custom_json", get_refresh_token=False)
# replace test with our wallet password
wallet_password = getpass.getpass('Wallet-Password:')
c.dpay.wallet.unlock(wallet_password)


@app.route('/')
def index():
    login_url = c.get_login_url(
        "http://localhost:5000/welcome",
    )
    return "<a href='%s'>Login with DPayId</a>" % login_url


@app.route('/welcome')
def welcome():
    access_token = request.args.get("access_token", None)
    name = request.args.get("username", None)
    if c.get_refresh_token:
        code = request.args.get("code")
        refresh_token = c.get_access_token(code)
        access_token = refresh_token["access_token"]
        name = refresh_token["username"]
    elif name is None:
        c.set_access_token(access_token)
        name = c.me()["name"]

    if name in c.dpay.wallet.getPublicNames():
        c.dpay.wallet.removeTokenFromPublicName(name)
    c.dpay.wallet.addToken(name, access_token)
    return "Welcome <strong>%s</strong>!" % name
