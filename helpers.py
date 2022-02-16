import certifi
import requests
from config import *
from pymongo import MongoClient


def mongo_client_connect():
    client = MongoClient(
        mongo_string,
        # The following not in mongodb atlas docs, need to install and import certifi and add next line
        tlsCAFile=certifi.where()
    )
    print('Connected to client')
    return client


def query_imdb(search_query):
    # TODO add all sensitive data to a git-ignore file and pass
    url = imdb_url
    querystring = {"q": search_query}
    headers = imdb_headers

    # Get the response from the api and retrieve the json from it
    r = requests.request("GET", url, headers=headers, params=querystring)
    json_data = r.json()

    # Get rid of unnecessary keys
    keys_to_remove = ['@meta', '@type', 'query', 'types']
    for key in keys_to_remove:
        json_data.pop(key, None)

    # Create list of items from 'results' key, only adding films and tv shows by checking for 'titleType' key
    titles = []
    for item in json_data['results']:
        if 'titleType' in item:
            titles.append(item)

    return titles


def save_to_db(checked_titles):
    client = mongo_client_connect()
    db = client.movie_collection
    movies = db.movies

    # Check if title exists, limit=1 stops search as soon as a match is found, no need to keep searching
    for title in checked_titles:
        if movies.count_documents({'id': title['id']}, limit=1):
            print('Title already exists')
        else:
            movies.insert_one(title)
            print('Title inserted')


def delete_from_db(movie_id):
    # Delete selected title from db
    client = mongo_client_connect()
    db = client.movie_collection
    movies = db.movies

    movies.delete_one({'id': movie_id})


def get_all_titles():
    titles = []

    client = mongo_client_connect()
    db = client.movie_collection
    collection = db.movies

    # Alphabetize dicts in array by title before returning
    cursor = collection.find({})
    for item in cursor:
        titles.append(item)

    sorted_titles = sorted(titles, key=lambda i: i['title'])

    return sorted_titles
