from collections import defaultdict
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
    for page_number in range(1,3):
        data = requests.get("https://api.themoviedb.org/3/trending/movie/week?api_key=8b6f1e2319a470dbc479bd4a3e4ac725&page={}".format(page_number)).json()['results']
        for item in data:
            provider_count = 0
            # print(item['id'])
            movie_data = requests.get(f"https://api.themoviedb.org/3/movie/{item['id']}?api_key=8b6f1e2319a470dbc479bd4a3e4ac725&language=en-US").json()
            watch_provider_data = data_watch_provider = requests.get(f"https://api.themoviedb.org/3/movie/{item['id']}/watch/providers?api_key=8b6f1e2319a470dbc479bd4a3e4ac725").json()['results']
            if 'US' not in data_watch_provider or 'flatrate' not in data_watch_provider['US']:
                None
            else:
                providers = data_watch_provider['US']['flatrate']
                p_list = []
                genre_list = []
                for i in providers:
                    for j in accepted_providers:
                        if i['provider_name'] == j:
                            provider_count += 1
                            p_list.append(j)
                if provider_count >= 1:
                    data_dict = defaultdict()
                    data_dict['title'] = movie_data['original_title']               # title
                    data_dict['poster_path'] = movie_data['poster_path']            # movie poster
                    data_dict['overview'] = movie_data['overview']                  # movie description
                    full_date = movie_data['release_date']
                    year = full_date[0:full_date.index("-")]
                    data_dict['release_date'] = year                                # release_date/year
                    round_vote_avg = "{:.1f}".format(movie_data['vote_average'])
                    data_dict['vote_average'] = round_vote_avg                      # ratings
                    total_mins = movie_data['runtime']
                    hours_mins = "{}hr:{}min".format(*divmod(total_mins, 60))       # movie runtime
                    data_dict['runtime'] = hours_mins
                    data_dict['provider_name'] = p_list         # subcription providers
                    for x in movie_data['genres']:
                        genre_list.append(x['name'])
                    data_dict['genres'] = genre_list
                    data_list.append(data_dict)
                else:
                    None 
    return render_template('home.html.j2', data=data_list)



@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.route('/advanced_search')
def advanced_search():
    return render_template('/advanced_search.html.j2')

