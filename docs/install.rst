.. _install:

Installation
============

Installing/Upgrading From the PyPI
----------------------------------
::

    $ pip install -U textblob
    $ python -m textblob.download_corpora

This will install TextBlob and download the necessary NLTK corpora. If you need to change the default download directory set the ``NLTK_DATA`` environment variable.

.. admonition:: Downloading the minimum corpora

    If you only intend to use TextBlob's default models (no model overrides), you can pass the ``lite`` argument. This downloads only those corpora needed for basic functionality.
    ::

        $ python -m textblob.download_corpora lite

With conda
----------

TextBlob is also available as a `conda <http://conda.pydata.org/>`_ package. To install with ``conda``, run ::

    $ conda install -c conda-forge textblob
    $ python -m textblob.download_corpora

From Source
-----------

TextBlob is actively developed on Github_.

You can clone the public repo: ::

    $ git clone https://github.com/sloria/TextBlob.git

Or download one of the following:

* tarball_
* zipball_

Once you have the source, you can install it into your site-packages with ::

    $ python setup.py install

.. _Github: https://github.com/sloria/TextBlob
.. _tarball: https://github.com/sloria/TextBlob/tarball/master
.. _zipball: https://github.com/sloria/TextBlob/zipball/master


Get the bleeding edge version
-----------------------------

To get the latest development version of TextBlob, run
::

    $ pip install -U git+https://github.com/sloria/TextBlob.git@dev


Migrating from older versions (<=0.7.1)
---------------------------------------

As of TextBlob 0.8.0, TextBlob's core package was renamed to ``textblob``, whereas earlier versions used a package called ``text``. Therefore, migrating to newer versions should be as simple as rewriting your imports, like so:

New:
::

    from textblob import TextBlob, Word, Blobber
    from textblob.classifiers import NaiveBayesClassifier
    from textblob.taggers import NLTKTagger

Old:
::

    from text.blob import TextBlob, Word, Blobber
    from text.classifiers import NaiveBayesClassifier
    from text.taggers import NLTKTagger


Python
++++++

TextBlob supports Python >=2.7 or >=3.5.


Dependencies
++++++++++++

TextBlob depends on NLTK 3. NLTK will be installed automatically when you run ``pip install textblob`` or ``python setup.py install``.

Some features, such as the maximum entropy classifier, require `numpy`_, but it is not required for basic usage.

.. _numpy: http://www.numpy.org/

.. _NLTK: http://nltk.org/
