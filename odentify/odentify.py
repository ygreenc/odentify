#!/usr/bin/env python

import click
import requests

API_URL = 'http://omdbapi.com'


class Formatter(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        self.available_types = {
            'list': self.as_list,
            'csv': self.as_csv,
            'format': self.as_string
        }

        if not self.type:
            self.type = 'list'

        if self.separator:
            self.type = 'csv'

        if self.format:
            self.type = 'format'

        if self.type not in self.available_types:
            raise KeyError('Format text %s not found' % type)

    def mprint(self, movie):
        return self.available_types[self.type](movie)

    def as_list(self, movie):
        for key, value in movie.items():
            click.echo('%s %s' % (key, value))

    def as_csv(self, movie):
        if not self.separator:
            click.echo(';'.join(movie.values()))

        click.echo(self.separator.join(movie.values()))

    def as_string(self, movie):
        if not self.format:
            click.echo(movie['Title'])
        click.echo(self.format.format(**movie))


pass_formatter = click.make_pass_decorator(Formatter)


def search_movie(movie_name):
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
@click.option('--type', default='list', show_default=True)
@click.option('--format', default=None)
@click.option('--separator')
@click.pass_context
def cli(ctx, **kwargs):
    try:
        ctx.obj = Formatter(**kwargs)
    except KeyError as e:
        print(e)
        exit(1)


@cli.command()
@click.argument('movie', required=True)
@pass_formatter
def search(formatter, movie):
    movies = search_movie(movie)
    for movie in movies:
        formatter.mprint(movie)
        click.echo()


@cli.command()
@click.argument('movie_id', required=True)
@pass_formatter
def fetch(formatter, movie_id):
    movie = fetch_movie(movie_id)
    formatter.mprint(movie)


if __name__ == '__main__':
    try:
        cli()
    except requests.exceptions.ReadTimeout as e:
        print("Request timed-out. The service might be unavailable or you've been banned")
        exit(1)
    except KeyError as k:
        print("Cannot find key {}".format(k))
        exit(1)
