#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Downloads the minimum necessary NLTK models and corpora required to support
TextBlob's basic features. Use this script if you only intend to use
TextBlob's default models. If you want to use other models, use
download_corpora.py. Modify for your own needs.
'''
from textblob.packages import nltk

REQUIRED_CORPORA = [
    'brown',  # Required for FastNPExtractor
    'punkt',  # Required for WordTokenizer
    'wordnet' # Required for lemmatization
]

def main():
    for each in REQUIRED_CORPORA:
        print('Downloading "{0}"'.format(each))
        nltk.download(each)
    print("Finished.")

if __name__ == '__main__':
    main()
