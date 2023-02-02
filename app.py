from flask import Flask, request, render_template
from flask.views import View
import requests

app = Flask(__name__)


class HomeView(View):
    methods = [ "POST", "GET"]
    def dispatch_request(self):
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        cur_list = [cur for cur in data['rates']]
        
        if request.method == "GET":
            return render_template("index.html", cur_list=cur_list)
        
        elif request.method == "POST":
            # Get the user's inputs
            amount = float(request.form["amount"])
            input_currency = request.form["input_currency"]
            output_currency = request.form["output_currency"]
            user_curs = [amount, input_currency, output_currency]

            # Call the API to get the exchange rate
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{input_currency}")
            data = response.json()
            exchange_rate = data["rates"][output_currency]

            # Calculate the converted amount
            results = exchange_rate * amount
            print(results)

            # Return the result to the user

            return render_template("index.html", cur_list=cur_list, results=results, user_curs=user_curs)


app.add_url_rule("/", view_func=HomeView.as_view(name="index"))




if __name__ == "__main__":
    app.run(debug=True)

