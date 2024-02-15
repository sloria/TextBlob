Contributing guidelines
=======================

In General
----------

- `PEP 8`_, when sensible.
- Conventions *and* configuration.
- TextBlob wraps functionality in NLTK and pattern.en. Anything outside of that should be written as an extension.
- Test ruthlessly. Write docs for new features.
- Even more important than Test-Driven Development--*Human-Driven Development*.
- These guidelines may--and probably will--change.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/


In Particular
-------------

Questions, Feature Requests, Bug Reports, and Feedback. . .
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

. . .should all be reported on the `Github Issue Tracker`_ .

.. _`Github Issue Tracker`: https://github.com/sloria/TextBlob/issues?state=open

Setting Up for Local Development
++++++++++++++++++++++++++++++++

1. Fork TextBlob_ on Github. ::

    $ git clone https://github.com/sloria/TextBlob.git
    $ cd TextBlob

2. Install development requirements. It is highly recommended that you use a virtualenv. ::

    # After activating your virtualenv
    $ pip install -r dev-requirements.txt

3. Install TextBlob in develop mode. ::

   $ python setup.py develop

.. _extension-development:

Developing Extensions
+++++++++++++++++++++

Extensions are packages with the name ``textblob-something``, where "something" is the name of your extension. Extensions should be imported with ``import textblob_something``.

Model Extensions
++++++++++++++++

To create a new extension for a part-of-speech tagger, sentiment analyzer, noun phrase extractor, classifier, tokenizer, or parser, simply create a module that has a class that implements the correct interface from ``textblob.base``. For example, a tagger might look like this:

.. code-block:: python

    from textblob.base import BaseTagger


    class MyTagger(BaseTagger):
        def tag(self, text):
            pass
            # Your implementation goes here

Language Extensions
+++++++++++++++++++

The process for developing language extensions is the same as developing model extensions. Create your part-of-speech taggers, tokenizers, parsers, etc. in the language of your choice. Packages should be named ``textblob-xx`` where "xx" is the two- or three-letter language code (`Language code reference`_).

.. _Language code reference: http://www.loc.gov/standards/iso639-2/php/code_list.php

To see examples of existing extensions, visit the :ref:`Extensions <extensions>` page.

Check out the :ref:`API reference <api_base_classes>` for more info on the model interfaces.


Git Branch Structure
++++++++++++++++++++

TextBlob loosely follows Vincent Driessen's `Successful Git Branching Model <http://http://nvie.com/posts/a-successful-git-branching-model/>`_ . In practice, the following branch conventions are used:

``dev``
    The next release branch.

``master``
    Current production release on PyPI.

Pull Requests
++++++++++++++

1. Create a new local branch.
::

    $ git checkout -b name-of-feature

2. Commit your changes. Write `good commit messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
::

    $ git commit -m "Detailed commit message"
    $ git push origin name-of-feature

3. Before submitting a pull request, check the following:

- If the pull request adds functionality, it is tested and the docs are updated.
- If you've developed an extension, it is on the :ref:`Extensions List <extensions>`.
- You've added yourself to ``AUTHORS.rst``.

4. Submit a pull request to the ``sloria:dev`` branch.

Running tests
+++++++++++++

To run all the tests: ::

    $ pytest

To skip slow tests: ::

    $ pytest -m 'not slow'

Documentation
+++++++++++++

Contributions to the documentation are welcome. Documentation is written in `reStructuredText`_ (rST). A quick rST reference can be found `here <https://docutils.sourceforge.io/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs and run in watch mode: ::

    $ tox -e watch-docs

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructuredText`: https://docutils.sourceforge.io/rst.html

.. _TextBlob: https://github.com/sloria/TextBlob
