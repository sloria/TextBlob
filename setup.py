try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'name': 'text.blob',
    'description': 'Simple, Pythonic text processing',
    'author': 'Steve Loria',
    'url': 'https://github.com/sloria/text.blob',
    'author_email': 'sloria1@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'nltk'],
    "tests_require": ['nose'],
    'packages': ['text.blob'],
    'py_modules': [],
}

setup(**config)
