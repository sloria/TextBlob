#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import webbrowser

from invoke import task

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')

@task
def test(ctx):
    ctx.run("python run_tests.py", pty=True)


@task
def clean(ctx):
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")
    ctx.run("rm -rf textblob.egg-info")
    clean_docs(ctx)
    print("Cleaned up.")

@task
def clean_docs(ctx):
    ctx.run("rm -rf %s" % build_dir)


@task
def browse_docs(ctx):
    path = os.path.join(build_dir, 'index.html')
    webbrowser.open_new_tab(path)

@task
def docs(ctx, clean=False, browse=False):
    if clean:
        clean_docs(ctx)
    ctx.run("sphinx-build %s %s" % (docs_dir, build_dir), pty=True)
    if browse:
        browse_docs(ctx)

@task
def readme(ctx, browse=False):
    ctx.run("rst2html.py README.rst > README.html", pty=True)
    if browse:
        webbrowser.open_new_tab('README.html')

@task
def doctest(ctx):
    os.chdir(docs_dir)
    ctx.run("make doctest")
