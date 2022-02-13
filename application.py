import json
import os
from flask import Flask, redirect, render_template, request
from adyen_session import createAdyenSession;

application = Flask(__name__)


# home page
@application.route("/")
def index():
    return redirect("/cart")

# cart - select country and amount of trees
@application.route("/cart")
def cart():
    return render_template("cart.html")

# checkout - embeds drop-in, collect payment details, confirm payment
@application.route("/checkout")
def checkout():
    amount = request.args.get("amount")

    # convert amount of trees to money
    # (a proper calculation would be better, but this will work for now)
    amount = int(amount) * 5 * 100

    return render_template("checkout.html", client_key=os.environ.get("ADYEN_CLIENT_KEY"), amount=amount)

@application.route("/session", methods=['POST'])
def payment_session():
    amount = json.loads(request.data)["amount"]
    
    return createAdyenSession(
        host_url = request.host_url, 
        amount=amount 
        )

@application.route("/result")
def checkout_complete():
    # print (request)
    return render_template("checkout-complete.html", result_code = request.args.get("code"))


if __name__ == '__main__':
    application.run(debug=True, port=8080, host='0.0.0.0')