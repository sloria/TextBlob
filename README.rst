TextBlob
========

Requirements
------------
- Python >= 2.7, but not Python 3 (yet)

Installation
------------
Just run: ::

    $ pip install textblob && download_corpora.py

Best to see that everything is working by running: ::

    $ nosetests

Usage
-----
Simple.

.. code-block:: python

    from text.blob import TextBlob

    text = """Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    """

    zen = TextBlob(text) # Create a new TextBlob
    # Get the part-of-speech tags
    zen.pos_tags         # [('beautiful', 'JJ'), ('is', 'VBZ'), ('better', 'RBR'),
                         # ('than', 'IN'), ('ugly', 'RB'), ...]
    # Get the noun_phrases
    zen.noun_phrases     # ['beautiful', 'explicit', 'simple', 'complex', 'flat',
                         # 'sparse', 'readability', 'special cases',
                         # 'practicality beats purity', 'errors', 'unless',
                         # 'obvious way','dutch', '*right* now', 'bad idea',
                         # 'good idea', 'namespaces', 'great idea']

    # Get word and noun phrase frequencies
    zen.word_counts['better']    # 10
    zen.word_counts['idea']      # 3
    zen.np_counts['great idea']  # 1

    # Get the start and end indices of sentences within a blob
    # This is useful for text highlighting, for example
    for sentence in blob.sentences:
        print(sentence)  # Beautiful is better than ugly
        print("---- Starts at index {}, Ends at index {}"\
                    .format(sentence.start_index, sentence.end_index))  # 0, 30

    # TextBlobs are like Python strings!
    zen[0:19]            # TextBlob("Beautiful is better")
    zen.upper()          # TextBlob("BEAUTIFUL IS BETTER THAN UGLY...")
    zen.find("purity")   # 293

    blob1 = TextBlob('apples')
    blob2 = TextBlob('bananas')
    blob1 < blob2            # True
    blob1 + ' and ' + blob2  # TextBlob('apples and bananas')

    # Get a serialized version of the blob (a list of dicts)
    zen.serialized       # [{'end_index': 30,
                         # 'noun_phrases': ['beautiful'],
                         # 'raw_sentence': 'Beautiful is better than ugly.',
                         # 'start_index': 0,
                         # 'stripped_sentence': 'beautiful is better than ugly'},

Testing
-------
Run :code:`$ nosetests` to run all tests.
