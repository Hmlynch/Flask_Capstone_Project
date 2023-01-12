from . import bp as app
from flask import Flask, render_template
from app.blueprints.auth.models import User
from flask_login import current_user
import requests
import json

# app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data_list = []
    accepted_providers = ['Netflix', 'Hulu', 'Amazon Prime Video', 'HBO Max', 'Disney Plus']
    provider_count = 0
    data = requests.get(f"https://api.themoviedb.org/3/trending/movie/week?api_key=8b6f1e2319a470dbc479bd4a3e4ac725").json()
    for item in data['results']:
        data_watch_provider = requests.get(f"https://api.themoviedb.org/3/movie/{item['id']}/watch/providers?api_key=8b6f1e2319a470dbc479bd4a3e4ac725").json()['results']
        if 'US' not in data_watch_provider or 'flatrate' not in data_watch_provider['US']:
            None
        else: 
            providers = data_watch_provider['US']['flatrate']
            for i in providers:
                for j in accepted_providers:
                    if i['provider_name'] == j:
                        provider_count += 1
            if provider_count >= 1:
                # information to display: ('title', 'poster_path', 'type', 'release_date', 'vote_average', 'runtime', 'provider_name', 'overview')
                data_dict = {}
                data_dict['title'] = item['title']
                data_dict['poster_path'] = item['poster_path']
                # data_dict['provider_name'] = i['provider_name']
                data_list.append(data_dict)
                print(data_list)
            else:
                None  
    return render_template('home.html.j2', data=data_list)


@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.route('/advanced_search')
def advanced_search():
    return render_template('/advanced_search.html.j2')

