#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "aradcliff"

import cProfile
import pstats
import functools
import timeit
import io
from pstats import SortKey


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return result
    return wrapper


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    if title in movies:
        return True


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    seen = {}
    duplicates = []

    for movie in movies:
        if movie not in seen:
            seen[movie] = 1
        else:
            if seen[movie] == 1:
                duplicates.append(movie)
            seen[movie] += 1
    return duplicates


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer('main()')
    r, n = 7, 3  # repeat, number constants
    result = t.repeat(repeat=r, number=n)
    min_of_averages = min(map(lambda x: x / n, result))
    return f"Best time across {r} repeats of {n} runs per repeat: {min_of_averages} sec"


def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))


if __name__ == '__main__':
    main()
