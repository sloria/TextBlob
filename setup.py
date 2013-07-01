import sys
import os

import text

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system("python setup.py register sdist upload")
    sys.exit()

if sys.argv[-1] == 'test':
    try:
        __import__('nose')
    except ImportError:
        print('nose required.')
        sys.exit(1)

    os.system('nosetests --verbosity 2')
    sys.exit()

def cheeseshopify(rst):
    '''Since PyPI doesn't support the `code-block` or directive, this replaces
    all `code-block` directives with `::`.
    '''
    ret = rst.replace(".. code-block:: python", "::")
    ret = ret.replace(":code:", "")
    return ret

with open('README.rst') as fp:
    long_desc = cheeseshopify(fp.read())

setup(
    name='textblob',
    version=text.__version__,
    description='Simple, Pythonic text processing. Sentiment analysis, '
                'POS tagging, noun phrase parsing, and more.',
    long_description=long_desc,
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/TextBlob',
    install_requires=['nltk', 'numpy'],
    packages=[
        'text'
    ],
    package_data = {
        "text": ["*.txt", "*.xml"],
    },
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    tests_require=['nose'],
)
