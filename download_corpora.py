#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Downloads the necessary NLTK models and corpora.'''
from nltk import download

REQUIRED_CORPORA = [
    'brown',
    'punkt',
]

def main():
    for each in REQUIRED_CORPORA:
        print(('Downloading "{0}"'.format(each)))
        download(each)
    print("Finished.")

if __name__ == '__main__':
    main()
