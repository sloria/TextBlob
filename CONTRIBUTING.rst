Contributing guidelines
=======================

In General
----------

- `PEP 8`_, when sensible.
- Test ruthlessly. Write docs for new features.
- Even more important than Test-Driven Development--*Human-Driven Development*.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/


In Particular
-------------

Questions, Feature Requests, Bug Reports, and Feedback. . .
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

. . .should all be reported on the `Github Issue Tracker`_ .

.. _`Github Issue Tracker`: https://github.com/sloria/TextBlob/issues?state=open

Setting Up for Local Development
++++++++++++++++++++++++++++++++

1. Fork TextBlob_ on Github.
2. Clone your fork::

    $ git clone git@github.com/yourusername/textblob.git

3. It is recommended that you use virtualenv to keep your environment clean. If you have virtualenv and virtualenvwrapper_, run ::

    $ mkvirtualenv textblob
    $ cd textblob
    $ workon textblob

- If you don't have virtualenv and virtualenvwrapper, you can install both using `virtualenv-burrito`_.

4. Install the development requirements. ::

    $ pip install -r dev-requirements.txt

Creating your own models
++++++++++++++++++++++++

You can add your own implementation for POS taggers, sentiment analyzers, chunkers, parsers, etc. simply by adding a class to the appropriate module in the ``text/`` package.

For example, if you want to create your own tagger, you would add a class to ``text/taggers.py``. The only requirement is that the class have a ``tag()`` method.

.. code-block:: python

    class MyTagger(BaseTagger):
        def tag(self, text):
            # Your implementation goes here


Check out the `API reference`_ for more info on the model interfaces.

.. _`API reference`: https://textblob.readthedocs.org/en/latest/api_reference.html

Git Branch Structure
++++++++++++++++++++

TextBlob loosely follows Vincent Driessen's `Successful Git Branching Model <http://http://nvie.com/posts/a-successful-git-branching-model/>`_ . In practice, the following branch conventions are used:

``dev``
    The next release branch.

``master``
    Current production release on PyPI.

Pull Requests
++++++++++++++

1. Create a new local branch. ::

    $ git checkout -b name-of-feature

2. Commit your changes. Write `good commit messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
::

    $ git commit -m "Detailed commit message"
    $ git push origin name-of-feature

3. Before submitting a pull request, check the following:

- If the pull request adds functionality, it should be tested and the docs should be updated.
- The pull request should work on Python 2.6, 2.7, 3.3, and PyPy. Use ``tox`` to verify that it does.
- You've added yourself to ``AUTHORS.rst``.

4. Submit a pull request to the ``sloria:dev`` branch.

Running tests
+++++++++++++

To run all the tests: ::

    $ python run_tests.py

To skip slow tests: ::

    $ python run_tests fast

To skip tests that require internet: ::

    $ python run_tests no-internet

To get test coverage reports (must have coverage installed): ::

    $ python run_tests cover

To run tests on Python 2.6, 2.7, and 3.3 virtual environments (must have each interpreter installed): ::

    $ tox

Documentation
+++++++++++++

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs: ::

    $ invoke build_docs -b

The ``-b`` (for "browse") automatically opens up the docs in your browser after building.

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html

.. _`virtualenv-burrito`: https://github.com/brainsik/virtualenv-burrito

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/

.. _TextBlob: https://github.com/sloria/TextBlob