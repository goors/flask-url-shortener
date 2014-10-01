import os
from flask import Flask
from controllers import api
from flask import json


app = Flask(__name__)
app.register_blueprint(api.api_methods)


app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='0209012'
    )
)
app.config.from_envvar("APP_SETTINGS", silent=True)


@app.errorhandler(404)
def page_not_found(e):
    response = {'response': "", 'status': 0, 'message': "Page not found"}
    return json.jsonify(response) , 404

@app.errorhandler(405)
def page_not_found(e):
    response = {'response': "", 'status': 0, 'message': "Method not allowed"}
    return json.jsonify(response) , 405



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
