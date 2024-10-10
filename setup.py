from setuptools import setup, find_packages

setup(
    name="textblob_complexity",  # Package name
    version="0.1",
    description="A text complexity scoring extension for TextBlob",
    packages=find_packages(where='src'),  # Include packages from the src directory
    package_dir={"": "src"},  # Tell setuptools where to find the package
    install_requires=["textblob", "nltk"],
)