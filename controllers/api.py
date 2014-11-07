from crossdomain import *

from model import *
import errors
from flask import Blueprint, jsonify, redirect, render_template
import  appconfig
api_methods = Blueprint('api_methods', __name__)

@api_methods.route('/', methods=['PUT'])
@crossdomain(origin='*')
def make_short_url():

    if 'url' in request.form :
        api_model = model()
        return api_model.make_short_url(request.form['url'])
    return jsonify({'message': errors.HACK, 'response': {}, 'status': '0'})



@api_methods.route('/', methods=['POST'])
@crossdomain(origin='*')
def get_stats():

    if 'url' in request.form :

        api_model = model()
        return api_model.get_url_stats(request.form['url'])
    return jsonify({'message': errors.HACK, 'response': {}, 'status': '0'})

@api_methods.route('/<url>', methods=['GET'])
def redirectto(url=None):

    print url

    if url != 'favicon.ico' and url != 'docs' and url != "docs/stats":
        api_model = model()
        new_url = api_model.redirect(url)
        if new_url is not False:
            return redirect(new_url)
        return jsonify({'message': errors.ERROR, 'response': {}, 'status': '0'})

    if url == 'docs':
        return render_template('home/docs.html', version=appconfig.VERSION)
    else:
        return render_template('home/stats.html', version=appconfig.VERSION)



@api_methods.route('/', methods=['GET'])
def index():

    return render_template('home/index.html', version=appconfig.VERSION)




