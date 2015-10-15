#!/usr/bin/env python

import requests

API_URL = 'http://omdbapi.com'


def search_movie(movie_name):
    response = requests.get(
        API_URL,
        params={
            's': movie_name,
            'r': 'json'})
    return response.json()['Search']


def fetch_movie(fetching_id):
    if fetching_id.startswith('tt'):
        # IMDB id has been passed for fetching
        params = {'i': fetching_id}
    else:
        # Search with title
        params = {'t': fetching_id}

    response = requests.get(API_URL, params=params).json()

    if response['Response'] == 'False':
        return None

    return response


def main():
    pass

if __name__ == '__main__':
    main()
