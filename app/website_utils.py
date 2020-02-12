#!/usr/bin/python
# coding=utf-8
import time
from urllib import parse


def sleep(time_secs=5):
    time.sleep(time_secs)


def compare_url_paths(actual, expected):
    def get_path(url):
        url = parse.urlparse(url)
        return url.path.replace('/', '')

    actual_path = get_path(actual)
    expected_path = get_path(expected)

    return True if actual_path == expected_path else False
