#!/usr/bin/env python

import click
import requests

import functools

API_URL = 'http://omdbapi.com'


def as_list(movie):
    """Output the movie as a list of attributes."""
    for key, value in sorted(movie.items()):
        click.echo('%s %s' % (key, value))


def as_string(movie, out_format="{Title}{Year}"):
    """Output movie according to format passed by user."""
    click.echo(out_format.format(**movie))


selected_formatting = as_list


def search_movie(movie_name):
    """Search for string on OMDB."""
    response = requests.get(
        API_URL,
        params={
            's': movie_name,
            'r': 'json',
            't': 'movie'
        },
        timeout=3.0
    )
    return response.json()['Search']


def fetch_movie(fetching_id):
    """Fetch movie attributes on OMDB."""
    if fetching_id.startswith('tt'):
        # IMDB id has been passed for fetching
        params = {'i': fetching_id}
    else:
        # Search with title
        params = {'t': fetching_id}

    response = requests.get(API_URL, params=params, timeout=3.0).json()

    if response['Response'] == 'False':
        return None

    return response


@click.group()
@click.option('--format', default=None)
@click.pass_context
def cli(ctx, format=None):
    global selected_formatting
    if format:
        selected_formatting = functools.partial(as_string, out_format=format)


@cli.command()
@click.argument('movie', required=True)
def search(movie):
    selected_formatting
    movies = search_movie(movie)
    for movie in movies:
        selected_formatting(movie)
        click.echo()


@cli.command()
@click.argument('movie_id', required=True)
def fetch(movie_id):
    movie = fetch_movie(movie_id)
    selected_formatting(movie)


if __name__ == '__main__':
    try:
        cli()
    except requests.exceptions.ReadTimeout as e:
        print("Request timed-out. Might be down or you could be banned!")
        exit(1)
