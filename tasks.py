import os
from invoke import task, run

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')

@task
def test():
    run("python run_tests.py", pty=True)

@task
def deps():
    print("Vendorizing nltk...")
    run("git clone https://github.com/nltk/nltk.git")
    run("rm -rf text/nltk")
    run("mv nltk/nltk text/")
    run("rm -rf nltk")

@task
def clean():
    run("rm -rf build")
    run("rm -rf dist")
    run("rm -rf textblob.egg-info")
    clean_docs()
    print("Cleaned up.")

@task
def clean_docs():
    run("rm -rf %s" % build_dir)

@task
def browse_docs():
    run("open %s" % os.path.join(build_dir, 'index.html'))

@task
def docs(clean=False, browse=False):
    if clean:
        clean_docs()
    run("sphinx-build %s %s" % (docs_dir, build_dir), pty=True)
    if browse:
        browse_docs()

@task
def readme():
    run("rst2html.py README.rst > README.html", pty=True)
    run("open README.html")

@task
def doctest():
    os.chdir(docs_dir)
    run("make doctest")
