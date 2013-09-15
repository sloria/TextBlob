.. _install:

Installation
============

Installing/Upgrading From the PyPI
----------------------------------
::

    $ pip install -U textblob
    $ curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python

This will install TextBlob and download the necessary NLTK corpora.

.. admonition:: Downloading the minimum corpora

    If you only intend to use TextBlob's default models (no model overrides), then you can use the ``download_corpora_lite.py`` script instead. This downloads only those corpora needed for basic functionality.
    ::

        $ curl https://raw.github.com/sloria/TextBlob/master/download_corpora_lite.py | python

.. admonition:: If you don't have pip:

    If you don't have ``pip`` (you should), run this first: ::

        $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python


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

Getting Extra Models and Data
-----------------------------

.. module:: text.taggers

Some features, such as the :class:`PerceptronTagger <PerceptronTagger>`, require data that is not available from the NLTK downloader. These data will be made available on the Github `release page`_ for TextBlob.

To install a model or corpus:

1. Download the file from the `release page`_.
2. Unzip/untar the downloaded file.
3. Place the uncompressed file in your TextBlob installation directory. To find out where this is, you can run ::

    $ python -c "import text; print(text.__path__[0])"

.. _release page: https://github.com/sloria/TextBlob/releases

Python
++++++

TextBlob supports Python >=2.6 or >=3.3.


Dependencies
++++++++++++

PyYAML is TextBlob's only external dependency. It will be installed automatically when you run ``pip install textblob`` or ``python setup.py install``. A vendorized version of NLTK_ is bundled internally.

.. _NLTK: http://nltk.org/


