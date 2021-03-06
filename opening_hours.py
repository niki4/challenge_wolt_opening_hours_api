from flask import Flask, abort, request, redirect, url_for

from examples import example_input, example_output
from helpers import validate_shifts, format_opening_hours_as_text

app = Flask(__name__)


def show_shifts_endpoint_instructions():
    return f"""
        <html>
        <head><title>Opening Hours</title></head>
        <body>
            <p>Send POST request with JSON string to parse, e.g.</p>
            <code>curl --header "Content-Type: application/json" \
                  --request POST --data '{example_input}' \
                  http://localhost:5000/shifts</code>
            <p>The result will be as below:</p>
            <pre>{example_output}</pre>
        </body>
        </html>
        """


@app.route('/')
def index():
    return redirect(url_for('shifts'))


@app.route("/shifts", methods=["GET", "POST"])
def shifts():
    if request.method == "POST":
        json_data = request.get_json()  # raise and return "bad request" if non-valid JSON
        errors = validate_shifts(json_data)
        if errors:
            abort(400, description="\n".join(errors))
        return format_opening_hours_as_text(json_data)
    else:
        return show_shifts_endpoint_instructions()
