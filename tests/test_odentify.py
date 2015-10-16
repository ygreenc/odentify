#!/usr/bin/env python

import unittest
from odentify import odentify

class MovieFetcher(unittest.TestCase):

    def testWImdbId(self):
        """Should find correct movie if passing imdb id"""
        movie = odentify.fetch_movie('tt0816692')
        self.assertEqual('Interstellar', movie['Title'])

    def testWMovieName(self):
        """Should find correct movie with title"""
        movie = odentify.fetch_movie('Interstellar')
        self.assertEqual('tt0816692', movie['imdbID'])

    def testMovieWSpecialChars(self):
        movie = odentify.fetch_movie('Cannibal! The Musical')
        self.assertEqual('tt0115819', movie['imdbID'])

    def testWinvalidImdbId(self):
        """Should return null if movie is not found by imdb id"""
        movie = odentify.fetch_movie('tt0000000')
        self.assertIsNone(movie)

    def testNonExistentMovieName(self):
        """Should return null if movie is not found by name"""
        movie = odentify.fetch_movie('This is not a real movie name doofus')
        self.assertIsNone(movie)


class MovieSearcher(unittest.TestCase):

    def testFileSharingFilename(self):
        pass

    def testRegulardMovieName(self):
        """Should find multiple hits for a common movie name"""
        results = odentify.search_movie('Django Unchained')
        self.assertGreaterEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
