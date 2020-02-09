#!/usr/bin/python
# coding=utf-8
import logging
import sys


def setup():
    # Setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
