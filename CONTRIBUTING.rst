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
- The pull request works on Python 2.7, 3.4, 3.5, 3.6, and PyPy. Use ``tox`` to verify that it does.
- You've added yourself to ``AUTHORS.rst``.

4. Submit a pull request to the ``sloria:dev`` branch.

Running tests
+++++++++++++

To run all the tests: ::

    $ python run_tests.py

To skip slow tests: ::

    $ python run_tests.py fast

To skip tests that require internet: ::

    $ python run_tests.py no-internet

To get test coverage reports (must have coverage installed): ::

    $ python run_tests.py cover

To run tests on Python 2.7, 3.4, 3.5, and 3.6 virtual environments (must have each interpreter installed): ::

    $ tox

Documentation
+++++++++++++

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs: ::

    $ invoke docs -b

The ``-b`` (for "browse") automatically opens up the docs in your browser after building.

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html

.. _TextBlob: https://github.com/sloria/TextBlob
