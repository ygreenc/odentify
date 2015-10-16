#!/usr/bin/env python

import click
import requests

API_URL = 'http://omdbapi.com'


def search_movie(movie_name):
    response = requests.get(
        API_URL,
        params={
            's': movie_name,
            'r': 'json',
            't': 'movie'
        }
    )
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


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@cli.command()
@click.argument('movie', required=True)
def search(movie):
    movies = search_movie(movie)
    for movie in movies:
        click.echo(movie['Title'])
        for key, value in movie.items():
            click.echo('%s %s' % (key, value))
        click.echo()


@cli.command()
@click.argument('movie_id', required=True)
def fetch(movie_id):
    movie = fetch_movie(movie_id)
    for key, value in movie.items():
        click.echo('%s %s' % (key, value))


if __name__ == '__main__':
    cli()
