#!/usr/bin/env python
# -*- coding: utf-8 -*-

from text.blob import TextBlob
def main():
    blob = TextBlob('this is the best library ever!')
    print(blob.sentiment)

if __name__ == '__main__':
    main()
